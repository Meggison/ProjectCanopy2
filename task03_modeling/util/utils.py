import rasterio as rio
import os
from rasterio.warp import calculate_default_transform, reproject, Resampling
from shutil import copyfile
from sklearn.model_selection import train_test_split

import glob2


class DataPreprocessing:
    src_crs = 'EPSG:4326'
    dst_crs = 'EPSG:32636'

    @staticmethod
    def get_and_copy_files(src_dir, tgt_dir):
        os.makedirs(tgt_dir, exist_ok=True)
        src_list = os.listdir(src_dir)
        for file in src_list:
            copyfile(os.path.join(src_dir, file), os.path.join(tgt_dir, file))
        tgt_list = list(glob2.glob(os.path.join(tgt_dir,'*.tif')))
        src_list = list(glob2.glob(os.path.join(src_dir,'*.tif')))
        src_list.sort()
        tgt_list.sort()
        return src_list, tgt_list

    @staticmethod
    def split_data(images_dir, masks_dir, train_size, random_state=42):
        """
        Splits image and mask data into training and validation sets.

        Args:
            images_dir (str): Path to the directory containing image files.
            masks_dir (str): Path to the directory containing mask files.
            train_size (float, optional): Proportion of data for the training set (default: 0.7).
            random_state (int, optional): Random seed for splitting (default: 42).

        Returns:
            tuple: A tuple of four lists containing training and validation image and mask filenames.
                - train_images (list): List of training image filenames.
                - val_images (list): List of validation image filenames.
                - train_masks (list): List of training mask filenames.
                - val_masks (list): List of validation mask filenames.
        """

        # Get list of image and mask filenames
        image_files = os.listdir(images_dir)
        mask_files = os.listdir(masks_dir)

        # Remove any non-image files
        image_files = [file for file in image_files if file.endswith('.tif')]
        mask_files = [file for file in mask_files if file.endswith('.tif')]

        # Ensure corresponding image and mask files match (optional but recommended)
        image_files.sort()
        mask_files.sort()
        for i in range(len(mask_files)):
            if image_files[i].replace('image_','') != mask_files[i]:
                print("name Mismatch!!")

        # Split filenames into train and validation sets
        train_images, val_images, train_masks, val_masks = train_test_split(
            image_files, mask_files, train_size=train_size, random_state=random_state
        )

        return train_images, val_images, train_masks, val_masks
    
    @staticmethod
    def move_files(src_dir, dst_root, dst_sub_dir, files):
        """
        Moves files from a source directory to a destination directory with a subdirectory.

        Args:
            src_dir (str): Path to the source directory containing files.
            dst_root (str): Path to the root directory for the destination.
            dst_sub_dir (str): Name of the subdirectory within dst_root to create and store files.
            files (list): List of filenames to move.
        """

        # Create subdirectory within dst_root if it doesn't exist
        os.makedirs(os.path.join(dst_root, dst_sub_dir), exist_ok=True)

        for file in files:
            src_path = os.path.join(src_dir, file)
            dst_path = os.path.join(dst_root, dst_sub_dir, file)
            copyfile(src_path, dst_path)

    @staticmethod
    def check(scenes, truths):
        for idx in range(len(scenes)):
            with rio.open(scenes[idx] , 'r') as scene:
            # Access CRS information
                scene_crs = scene.crs
                scene_bounds = scene.bounds
                transform = scene.transform
                left, bottom, right, top = scene_bounds
                x_min, y_min = rio.transform.rowcol(transform, left, bottom)
                x_max, y_max = rio.transform.rowcol(transform, right, top)

                # # Print the bounds in meters
                # print('Scene Bounds in meters:', x_min, y_min, x_max, y_max)
                # print(scene.bounds)

            with rio.open(truths[idx], 'r') as truth:
            # Access CRS information
                truth_crs = truth.crs
                truth_bounds = truth.bounds
                transform = truth.transform
                left, bottom, right, top = truth_bounds
                x_min, y_min = rio.transform.rowcol(transform, left, bottom)
                x_max, y_max = rio.transform.rowcol(transform, right, top)

                # # Print the bounds in meters
                # print('Truth Bounds in meters:', x_min, y_min, x_max, y_max)
                # print(truth.bounds)

            # print(rio.coords.disjoint_bounds(scene_bounds, truth_bounds))
            assert scene.bounds == truth.bounds

    @staticmethod
    def reproject_scenes_truths(truths, truth_reprojected, scenes, scenes_reprojected):
        for idx in range(len(truths)):
            #idx = 0
            with rio.open(truths[idx],'r') as truth_src:
                transform, width, height = calculate_default_transform(DataPreprocessing.src_crs, 
                                                                       DataPreprocessing.dst_crs, 
                                                                       truth_src.width, 
                                                                       truth_src.height, 
                                                                       *truth_src.bounds)
                truth_kwargs = truth_src.meta.copy()
                out_profile = truth_src.profile.copy()
                imgdata = np.array([truth_src.read(i) for i in truth_src.indexes])
                truth_kwargs.update({'crs': DataPreprocessing.dst_crs, 
                                     'transform': transform, 
                                     'width': width, 
                                     'height': height})

                new_affine = rio.Affine(10, 0, int(transform[2]), 0, -10, int(transform[5]))

                out_profile["transform"] = new_affine
                path_maskNew = truth_reprojected[idx]
                with rio.open(
                    path_maskNew,
                    mode="w",
                    driver="GTiff",
                    height=imgdata[0].shape[0],
                    width=imgdata[0].shape[1],
                    count=1,
                    dtype=imgdata.dtype,
                    crs=DataPreprocessing.dst_crs,
                    transform=out_profile["transform"],
                ) as new_dataset:
                    new_dataset.write(imgdata[0],1)
                    
                with rio.open(scenes[idx],'r') as scene_src:
                    src_transform = scene_src.transform
                    dst_transform = out_profile["transform"]

                    data = scene_src.read()

                    scene_kwargs = scene_src.meta
                    scene_kwargs['transform'] = dst_transform
                    scene_kwargs['width']= 128
                    scene_kwargs['height']= 128
                    scene_kwargs['crs'] = dst_crs

                    with rio.open(scenes_reprojected[idx], 'w',**scene_kwargs) as dst:
                        for i, band in enumerate(data, 1):
                            dest = np.zeros_like(band)

                            reproject(band, 
                                      dest, 
                                      src_transform=src_transform,
                                      src_crs=scene_src.crs, 
                                      dst_transform=dst_transform,
                                      dst_crs=DataPreprocessing.dst_crs,
                                      resampling=Resampling.nearest)

                            dst.write(dest, indexes=i)

class ModelTraining:
    @staticmethod
    def train_epoch(model, loss_fn, metrics, optimizer, train_loader, device, epochs, verbose=True):
        """
        Performs a single training epoch on the provided dataloader.

        Args:
            model: The segmentation model to train.
            loss_fn: The loss function to use for training (e.g., DiceLoss).
            metrics: A function or list of functions for calculating metrics (e.g., iou_score).
            optimizer: The optimizer to update the model parameters.
            train_loader: The dataloader containing the training data.
            device: The device to use for training (CPU or GPU).
            verbose: Whether to print training logs.

        Returns:
            A dictionary containing training logs (loss, metrics).
        """
        model.train()  # Set the model to training mode
        train_logs = {}
        total_loss = 0.0

        for batch_idx, batch_data in enumerate(train_loader):
            images, masks = batch_data['image'], batch_data['mask']
            images, masks = images.to(device), masks.to(device)  # Move data to device

            # Forward pass
            predictions = model(images)

            # Calculate loss
            loss = loss_fn(predictions, masks)

            # Backward pass and parameter update
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()  # accumulate loss

            if verbose and (batch_idx + 1) % 100 == 0:
                print(f'Epoch [{i + 1}/{epochs}], Step [{batch_idx + 1}/{len(train_loader)}], Loss: {loss.item():.4f}')

        train_logs['loss'] = total_loss / len(train_loader)

        # Calculate IoU metric 
        iou_score = metrics(predictions, masks)  # metrics is the iou_score function
        train_logs['iou_score'] = iou_score

        return train_logs
    
    @staticmethod
    def validate_epoch(model, loss_fn, metrics, val_loader, device, verbose=True):
        """
        Performs a single validation epoch on the provided dataloader.

        Args:
            model: The segmentation model to validate.
            loss_fn: The loss function to use for validation (e.g., DiceLoss).
            metrics: A function or list of functions for calculating metrics (e.g., iou_score).
            val_loader: The dataloader containing the validation data.
            device: The device to use for validation (CPU or GPU).
            verbose: Whether to print validation logs.

        Returns:
            A dictionary containing validation logs (loss, metrics).
        """
        model.eval()  # Set the model to evaluation mode
        val_logs = {}
        total_loss = 0.0

        with torch.no_grad():  # Disable gradient calculation for validation
            for images, masks in val_loader:
                images, masks = images.to(device), masks.to(device)

                # Forward pass
                predictions = model(images)

                # Calculate loss
                loss = loss_fn(predictions, masks)

                total_loss += loss.item()

                if verbose:
                    print(f'Validation Step: [{batch_idx + 1}/{len(val_loader)}]')

        val_logs['loss'] = total_loss / len(val_loader)

        # Calculate IoU metric
        iou_score = metrics(predictions, masks)  # metrics is the iou_score function
        val_logs['iou_score'] = iou_score

        return val_logs
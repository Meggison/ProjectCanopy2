import os
import torch
import lightning as L
import segmentation_models_pytorch as smp

# assumes a predefined torch model, loss function, and optimizer
class LightningModel(L.LightningModule):
    def __init__(self, base_model, optimizer, metric_dict):
        super().__init__()
        self.model = base_model
        # self.loss_fn = loss_fn
        self.optimizer = optimizer
        self.metric_dict = metric_dict

    def step(self, batch, batch_idx, mode, metric_dict):
        x, y = batch
        preds = self.model(x)[:, 1, :, :].unsqueeze(1)
        tmp_dict = {mode + "_" + k: v(preds, y) for k, v in metric_dict.items()}
        self.log_dict(
            tmp_dict,
            prog_bar=True)
        return tmp_dict[mode + "_" + "loss"]

    def training_step(self, batch, batch_idx):
        return self.step(batch, batch_idx, "train", self.metric_dict)
    
    def validation_step(self, batch, batch_idx):
        return self.step(batch, batch_idx, "val", self.metric_dict)
    
    def test_step(self, batch, batch_idx):
        return self.step(batch, batch_idx, "test", self.metric_dict)
    
    def predict_step(self, batch, batch_idx, dataloader_idx=0):
        return self(batch)
    
    def configure_optimizers(self):
        return self.optimizer

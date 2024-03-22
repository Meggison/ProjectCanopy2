import os
import torch
import pytorch_lightning as pl

# assumes a predefined torch model, loss function, and optimizer
class LightningModel(pl.LightningModule):
    def __init__(self, base_model, loss_fn, optimizer):
        super().__init__()
        self.model = base_model
        self.loss_fn = loss_fn
        self.optimizer = optimizer
    
    def step(self, batch, batch_idx, metric_name):
        x, y = batch
        preds = self.model(x)
        loss = self.loss_fn(preds, y)
        self.log(metric_name, loss)
        return loss

    def training_step(self, batch, batch_idx):
        return self.step(batch, batch_idx, "train_loss")
    
    def validation_step(self, batch, batch_idx):
        return self.step(batch, batch_idx, "val_loss")
    
    def test_step(self, batch, batch_idx):
        return self.step(batch, batch_idx, "test_loss")
    
    def configure_optimizers(self):
        return self.optimizer

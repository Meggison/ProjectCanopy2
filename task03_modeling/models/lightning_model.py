import os
import torch
import lightning as L

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
        preds = self.model(x)
        # loss = self.loss_fn(preds, y)
        # self.log(metric_name, loss, prog_bar=True)
        self.log_dict(
            {mode + "_" + k: v(preds, y) for k, v in metric_dict.items()},
            prog_bar=True)
        return metric_dict[mode + "_" + "loss"]

    def training_step(self, batch, batch_idx, metric_dict):
        return self.step(batch, batch_idx, "train", metric_dict)
    
    def validation_step(self, batch, batch_idx, metric_dict):
        return self.step(batch, batch_idx, "val", metric_dict)
    
    def test_step(self, batch, batch_idx, metric_dict):
        return self.step(batch, batch_idx, "test", metric_dict)
    
    def configure_optimizers(self):
        return self.optimizer

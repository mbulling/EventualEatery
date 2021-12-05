from torch.utils.data import Dataset
import torch
import torch.nn as nn
import torch.nn.functional as F

class BinaryDataset(Dataset):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __len__(self):
        return len(self.x)
    
    def __getitem__(self, index):
        features = self.x[index, :]
        labels = self.y[index, :]
        
        # we have feature columns 
        features = torch.tensor(features, dtype=torch.float32)
        # there are several classes and each class can have a binary value ...
        # ... either 0 or 1
        for x in range(len(labels)):
            labels[x] = torch.tensor(labels[x], dtype=torch.float32)
        
        dictionary = dict()
        dictionary['features'] = features
        for x in range(len(labels)):
            dictionary[('label' + x)] = labels[x]

        return dictionary

class MultiCategoryDataset(Dataset):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __len__(self):
        return len(self.x)
    
    def __getitem__(self, index):
        features = self.x[index, :]
        labels = self.y[index, :]
        
        features = torch.tensor(features, dtype=torch.float32)
        for x in range(len(labels)):
            labels[x] = torch.tensor(labels[x], dtype=torch.long)
        
        dictionary = dict()
        dictionary['features'] = features
        for x in range(len(labels)):
            dictionary[('label' + x)] = labels[x]

        return dictionary

class BinaryDataset(Dataset):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __len__(self):
        return len(self.x)
    
    def __getitem__(self, index):
        features = self.x[index, :]
        labels = self.y[index, :]
        
        # we have 12 feature columns 
        features = torch.tensor(features, dtype=torch.float32)
        # there are 5 classes and each class can have a binary value ...
        # ... either 0 or 1
        label1 = torch.tensor(labels[0], dtype=torch.float32)
        label2 = torch.tensor(labels[1], dtype=torch.float32)
        label3 = torch.tensor(labels[2], dtype=torch.float32)
        label4 = torch.tensor(labels[3], dtype=torch.float32)
        label5 = torch.tensor(labels[4], dtype=torch.float32)
        return {
            'features': features,
            'label1': label1,
            'label2': label2,
            'label3': label3,
            'label4': label4,
            'label5': label5,
        }

class MultiHeadBinaryModel(nn.Module):
    def __init__(self):
        super(MultiHeadBinaryModel, self).__init__()
        self.fc1 = nn.Linear(12, 32) # 12 is the number of features
        self.fc2 = nn.Linear(32, 64)
        self.fc3 = nn.Linear(64, 128)
        self.fc4 = nn.Linear(128, 256)
        
        # we will treat each head as a binary classifier ...
        # ... so the output features will be 1
        self.out1 = nn.Linear(256, 1)
        self.out2 = nn.Linear(256, 1)
        self.out3 = nn.Linear(256, 1)
        self.out4 = nn.Linear(256, 1)
        self.out5 = nn.Linear(256, 1)
    
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = F.relu(self.fc4(x))
        
        # each binary classifier head will have its own output
        out1 = F.sigmoid(self.out1(x))
        out2 = F.sigmoid(self.out2(x))
        out3 = F.sigmoid(self.out3(x))
        out4 = F.sigmoid(self.out4(x))
        out5 = F.sigmoid(self.out5(x))
        
        return out1, out2, out3, out4, out5

class MultiHeadMultiCategory(nn.Module):
    def __init__(self):
        super(MultiHeadMultiCategory, self).__init__()
        self.fc1 = nn.Linear(12, 32) # 12 is the number of features
        self.fc2 = nn.Linear(32, 64)
        self.fc3 = nn.Linear(64, 128)
        self.fc4 = nn.Linear(128, 256)
        
        # we will treat each head as a multi-category classifier ...
        # ... so the output features will be 2 (0 and 1)
        self.out1 = nn.Linear(256, 2)
        self.out2 = nn.Linear(256, 2)
        self.out3 = nn.Linear(256, 2)
        self.out4 = nn.Linear(256, 2)
        self.out5 = nn.Linear(256, 2)
    
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = F.relu(self.fc4(x))
        
        out1 = F.sigmoid(self.out1(x))
        out2 = F.sigmoid(self.out2(x))
        out3 = F.sigmoid(self.out3(x))
        out4 = F.sigmoid(self.out4(x))
        out5 = F.sigmoid(self.out5(x))
        
        return out1, out2, out3, out4, out5

def binary_loss_fn(outputs, targets):
    loss = 0
    for x in range(len(targets)):
        loss += nn.BCELoss()(outputs[x], targets[x])
    return loss / len(targets)

def multicat_loss_fn(outputs, targets):
    loss = 0
    for x in range(len(targets)):
        loss += nn.CrossEntropyLoss()(outputs[x], targets[x])
    return loss / len(targets)
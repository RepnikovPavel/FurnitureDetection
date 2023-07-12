import torch


class ModelController:
    model_ = None

    def __init__(self, model):
        '''
        accepts ref to model, torch.device, torch.device
        :param model:
        :param cpu_device: torch.device('cpu',index)
        :param gpu_device: torch.device('gpu',index)
        '''
        self.model_ = model

    def stop_controlling_the_model(self, to_device, set_train_or_eval):
        '''
         send model to device,
         switch model to train_or_eval
        :return: None
        '''
        self.model_.to(device = to_device)
        if set_train_or_eval=='train':
            self.model_.train()
        if set_train_or_eval=='eval':
            self.model_.eval()

    def __switch_model_to_eval(self):
        self.model_.eval()

    def __switch__model_to_train(self):
        self.model_.train()

    def __load_model_to(self, device):
        self.model_.to(device=device)

    def eval_model_on_batch(self, batch):
        '''

        :param batch: torch.tensor
        :return: model outpute on batch
        '''
        return self.model_(batch)

    def eval_model_on_the_list_of_elements(self,
                                           input_storage,
                                           output_storage,
                                           output_storage_device,
                                           run_on_device,
                                           batch_size):
        '''
        calculates the value of the model on the specified list,
        writes the model's responses to the specified list
        :param input_storage: storage for model input elements
        :param output_storage: storage for model responses
        :param batch_size:
        :param device: 'cpu','gpu'
        :return: None
        '''
        with torch.no_grad():
            self.__switch_model_to_eval()
            N = len(input_storage)
            num_of_batches = N // batch_size
            last_batch_size = N % batch_size
            device_for_eval = run_on_device
            self.__load_model_to(device_for_eval)
            for i in range(num_of_batches):
                batch = torch.stack(input_storage[i*batch_size:(i + 1)*batch_size]).to(device=device_for_eval)
                ans_on_batch = self.eval_model_on_batch(batch).to(device=output_storage_device)
                for j in range(batch_size):
                    output_storage.append(ans_on_batch[j])
            if last_batch_size > 0:
                last_batch = torch.stack(input_storage[num_of_batches*batch_size:]).to(device=device_for_eval)
                ans_on_last_batch = self.eval_model_on_batch(last_batch).to(device=output_storage_device)
                for j in range(last_batch_size):
                    output_storage.append(ans_on_last_batch[j])
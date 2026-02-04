import psutil
import torch
import time

class Router:
    def ___init__(self):
        self.cloud_rate_limit_counter = 0
        self.last_reset_time = time.time()
        
    def check_system_health(self):
        if torch.cuda.is_available():
            vram_free = torch.cuda.mem_get_info()[0] / 1024**3 # in GB
            if vram_free < 2.0:
                return "BUSY_LOCAL"
        
        if time.time() - self.last_reset_time > 60:
            self.cloud_rate_limit_counter = 0
            self.last_reset_time = time.time()
            
        if self.cloud_rate_limit_counter >= 15:
            return "BUSY_CLOUD"
            
        return "AVAILABLE"

    def route_request(self, local_ocr_confidence):
        status = self.check_system_health()
        

        
        
        if local_ocr_confidence < 0.60:
            if status == "BUSY_CLOUD":
                return "QUEUE" 
            self.cloud_rate_limit_counter += 1
            return "PATH_1_CLOUD"
            

        if status == "BUSY_LOCAL":
             if status != "BUSY_CLOUD":
                 self.cloud_rate_limit_counter += 1
                 return "PATH_1_CLOUD"
             else:
                 return "QUEUE"
                 

        return "PATH_2_LOCAL"
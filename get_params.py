class GetArguments():
    def __init__(self, args):
        self.args = args
        self.arg_dict = {}

    def add_default(self,arg_name, value):
        self.arg_dict.update({arg_name:value})

    def get_dnn_params(self):
        dnn_params = self.arg_dict
        dnn_params.pop("-i")
        dnn_params.pop("-o")
        return dnn_params
    
    def get_io_params(self):
        return self.arg_dict["-i"], self.arg_dict["-o"]

    def update_values(self):
        self.args.pop(0)
        if len(self.args) % 2 != 0:
            raise Exception("Wrong number of arguments")
        else:
            for i in range(len(self.args) // 2):
                if self.args[i*2] not in self.arg_dict:
                    raise Exception("Wrong argument " + self.args[i*2] + " - no such argument!")
                self.arg_dict[self.args[i*2]] = self.args[i*2+1]


class NotQuiteJson:
    class JsonStruct:
        def __init__(self, type, parent=None) -> None:
            self.type   = type
            self.parent = parent
            self.keys   = []
            self.values = []
            
        def build(self):
            if self.type == dict:
                data = {}
                for k, v in zip(self.keys, self.values):
                    data[k] = v
            elif self.type == list:
                data = self.values
            else:
                data = "".join(self.values)
                if data.isnumeric():
                    if not "." in data:
                        data = int(data)
                    else:
                        data = float(data)
                else: 
                    match data.lower():
                        case "false":
                            data = False
                        case "true":
                            data = True
                        case "none":
                            data = None
            return data
            
        def append_val(self, value):
            self.values.append(value)
            
        def append_key(self, key):
            self.keys.append(key)
                
        def is_string(self):
            return self.type == str
        
        def __repr__(self):
            if self.type == dict:
                return f"[Ks: ({self.keys}) Vs: ({self.values})]"
            elif self.type == list:
                return f"[Le:{str(self.values)}]"
            else:
                st = "".join(self.values)
                return f"[Str:{ st }]"
            
    def __init__(self, debug=False) -> None:
        self.debug = debug
        
    def parseIter(self, source_data: str):
        source_data  = source_data.replace("{}", "None").replace("[]", "None").replace("''", "None").replace('""', "None")
        stack = [self.JsonStruct(type=dict)]
        try:
            for char in source_data:
                match char:
                    case "{":
                        # new dict
                        stack.append(self.JsonStruct(type=dict, parent=stack[-1]))
                    case "[":
                        # new list
                        stack.append(self.JsonStruct(type=list, parent=stack[-1]))
                    case ":":
                        # key ends
                        key = stack.pop().build()
                        # Make sure the key is a string
                        stack[-1].append_key(str(key))
                    case _  :
                        # is a string
                        if char.isalnum():
                            if not stack[-1].is_string():
                                # Initialize new string if necessary
                                stack.append(self.JsonStruct(type=str, parent=stack[-1]))
                            # add char to current string
                            stack[-1].append_val(char)
                            
                        elif char in ["]", "}", ","]:
                            if len(stack) < 3:
                                print("End of struct list reached. Bracket Mismatch?")
                                return stack[-1].build()
                            # End of child structure. Pop from stack and add ref to parent
                            value = stack.pop().build() # Converts object class to data structure
                            parent = stack[-1]
                            if self.debug: print(f"Inserting {type(value)} '{value}' \nin {type(parent)} '{parent}'")
                            if not type(parent) == self.JsonStruct:
                                print(f"MISMATCH: Expected JsonStruct, got {type(parent)}")
                                break
                            else:
                                parent.append_val(value)
        except Exception as e:
            print("ERROR: ", e)
            print(char, stack)
        return stack[-1].build()

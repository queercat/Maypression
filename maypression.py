class Maypressor:
    __reversed_frequency_map = {}
    
    def __init__(self, uncompressed_text=""):
        self.__uncompressed_text = uncompressed_text
        self.__frequency_map = {}

        self.__compressed_text = ""
        self.__compression_map = {}

        self.__frequency_threshold = 8

    def __generate_frequency_map(self):
        for word in self.__uncompressed_text.split(" "):
            if word not in self.__frequency_map:
                self.__frequency_map[word] = 0
            
            self.__frequency_map[word] += 1

        for word in self.__frequency_map.keys():
            value = self.__frequency_map[word]

            if value not in self.__reversed_frequency_map:
                self.__reversed_frequency_map[value] = []

            self.__reversed_frequency_map[value].append(word)

        self.__generate_compression_map()

    def __generate_compression_map(self):
        for frequency in sorted(self.__reversed_frequency_map.keys())[::-1]:
            if frequency >= self.__frequency_threshold:
                for value in self.__reversed_frequency_map[frequency]:
                    self.__compression_map[value] = hex(len(self.__compression_map.keys()))[2:]

        self.__reverse_compression_map = {}

        for key in self.__compression_map.keys():
            self.__reverse_compression_map[self.__compression_map[key]] = key

    def compress(self, uncompressed_text: str = "") -> tuple((str, list)):
        if uncompressed_text != "":
            self.__uncompressed_text = uncompressed_text
     
        self.__generate_frequency_map()

        for word in self.__uncompressed_text.split(" "):
            if word in self.__compression_map.keys():
                self.__compressed_text += F"{self.__compression_map[word]}m"
            else:
                self.__compressed_text += F"[{word}]"

        return ((self.__compressed_text, self.__reverse_compression_map))

    def uncompress(self, compressed_text: str = "") -> str:
        uncompressed_text = ""
        bit_count = 0
        map_depth = 0


        map_index_start = compressed_text.rfind("{")
        map_index_end = compressed_text.rfind("}")


        compression_map = eval(compressed_text[map_index_start:map_index_end + 1])

        for idx, c in enumerate(compressed_text):            
            if idx == map_index_start:
                break
            
            if map_depth > 0:
                if c == "[":
                    map_depth += 1
                if c == "]":
                    map_depth -= 1
                
                if map_depth == 0:
                    uncompressed_text += F"{compressed_text[idx - bit_count + 1:idx]} "
                    bit_count = 0
                    pass
            
                bit_count += 1
            
            else:
                if c == "[":
                    map_depth += 1
                    bit_count = 0
                    pass

                if c == "]":
                    bit_count = 0
                
                if c == "m":
                    bit_count -= 1
                    uncompressed_text += F"{compression_map[compressed_text[idx - bit_count:idx]]} "
                    bit_count = 0
                    pass
            
                bit_count += 1
            
        print(uncompressed_text)

compressor = Maypressor()
contents = ""

# with open("big.txt", "r") as f:
#     for line in f:
#         contents += f.readline()

# com_text, com_map = compressor.compress(contents)

# print(com_map)

# with open("com.mp", "w") as mp:
#     mp.write(com_text)
#     mp.write(str(com_map))

# contents = ""

with open("com.mp", "r") as mp:
    contents = mp.read()

compressor.uncompress(contents)
import math

# Choosing the Cache Memory Mode
mode = input(">>1<< Single Cache Memory\n>>2<< Multilevel Cache Memory\n\nChoice - ")

# Single Cache Memory
if mode == "1":
    size_main = int(input("Enter the size of Main Memory - "))                         # Main Memory Size
    size_cache = int(input("Enter the size of Cache Memory - "))                       # Cache Memory Size
    words_per_block = int(input("Enter the number of words in each block - "))         # Words in each Block
    cache_lines = size_cache // words_per_block         # Number of Cache Lines
    blocks = size_main // words_per_block               # Number of Blocks
    address_bits = int(math.log(size_main, 2))          # Number of bits available for addressing

    MainMemory = {}          # Main Memory as a Dictionary

    for i, j in zip(range(0, size_main, words_per_block), range(blocks)):
        MainMemory["B" + str(j)] = []
        for x in range(words_per_block):

            MainMemory["B" + str(j)].append(["W" + str(i + x), bin(i + x).replace("0b", "").rjust(address_bits, "0"), j, x, i + x])

    CacheMemory = {}         # Cache Memory as a Dictionary

    for j in range(cache_lines):
        # Contents - Block, Address
        CacheMemory["C" + str(j)] = [None, None]

    word_bits = len(bin(words_per_block - 1).replace("0b", ""))       # Number of bits for word
    cl_bits = len(bin(cache_lines - 1).replace("0b", ""))             # Number of bits for cache lines
    tag_bits = address_bits - word_bits - cl_bits                     # Number of bits for tags

    # Mapping Method Selection
    c = input("\n>> 1 << Direct Mapping \n>> 2 << Associative Memory \n>> 3 << N - Way Set Associative Memory \n\nChoice - ")

    # Direct Mapping
    if c == "1":
        print("\nAddress Bits - " + str(address_bits))
        print("Words Bits - " + str(word_bits))
        print("Cache Line Bits - " + str(cl_bits))
        print("Tag Bits - " + str(tag_bits))

        while(True):
            c = input("\n>> 1 << Load a word into cache memory \n>> 2 << Search cache memory \n>> 3 << Exit \n\nChoice - ")

            # Loading
            if c == "1":
                address = input("\nEnter the address - ")
                word = int(address[-word_bits : ], 2)
                cache_line = int(address[tag_bits : tag_bits + cl_bits], 2)
                tag = address[ : tag_bits]
                block_number = int(address[ : tag_bits + cl_bits], 2)

                # If cache memory location is empty
                if CacheMemory["C" + str(cache_line)] == [None, None]:
                    CacheMemory["C" + str(cache_line)] = [MainMemory["B" + str(block_number)], address]   # Adding a copy of block to the cache line
                else:
                    # If cache memory location is being replaced with a new address
                    print("\nBlock Replacement! Address " + CacheMemory["C" + str(cache_line)][1] + " will be replaced by " + address + ".")
                    CacheMemory["C" + str(cache_line)] = [MainMemory["B" + str(block_number)], address]   # Adding a copy of block to the cache line
            # Searching
            elif c == "2":
                address = input("\nEnter the address - ")
                cache_line = int(address[tag_bits : tag_bits + cl_bits], 2)
                tag = address[ : tag_bits]

                if CacheMemory["C" + str(cache_line)] != [None, None]:
                    if CacheMemory["C" + str(cache_line)][1] == address:
                        print("\nCache Hit!")
                        print(f"Block Number - {int(address[ : tag_bits + cl_bits], 2)}")
                        print(f"Cache Line - {cache_line}")
                        Words = CacheMemory["C" + str(cache_line)]
                        W = ""

                        # Words present in the block
                        for i in range(words_per_block):
                            W += Words[0][i][0] + " "

                        print("Words - " + W)
                    else:
                        print("\nCache Miss!\nAddress in Cache Line was replaced by " + CacheMemory["C" + str(cache_line)][1] + ".")
                else:
                    print("\nCache Miss!\nCache Line is empty.")
            # Exit
            elif c == "3":
                print("\nEnded Successfully!")
                break
            # Wrong Selection
            else:
                print("Only choose among the provided options!")
    # Associative Mapping
    elif c == "2":
        print("\nAddress Bits - " + str(address_bits))
        print("Words Bits - " + str(word_bits))
        print("Tag Bits - " + str(address_bits - word_bits))
        counter = 0

        while (True):
            c = input("\n>> 1 << Load a word into cache memory \n>> 2 << Search cache memory \n>> 3 << Exit \n\nChoice - ")

            # Loading
            if c == "1":
                address = input("\nEnter the address - ")
                word = int(address[-word_bits : ], 2)
                tag = address[ : address_bits - word_bits]
                block_number = int(address[ : address_bits - word_bits], 2)

                if CacheMemory["C" + str(counter)] == [None, None]:
                    CacheMemory["C" + str(counter)] = [MainMemory["B" + str(block_number)], address]   # Adding a copy of block to the cache line
                else:
                    print("\nBlock Replacement! Address " + CacheMemory["C" + str(counter)][1] + " will be replaced by " + address + ".")
                    CacheMemory["C" + str(counter)] = [MainMemory["B" + str(block_number)], address]   # Adding a copy of block to the cache line

                counter += 1

                # FIFO replacement policy
                if counter == cache_lines:
                    counter = 0
            # Searching
            elif c == "2":
                address = input("\nEnter the address - ")
                tag = address[ : address_bits - word_bits]
                found = False

                # Iterating over all the cache lines
                for i in range(cache_lines):
                    if CacheMemory["C" + str(i)] != [None, None]:
                        if CacheMemory["C" + str(i)][1] == address:
                            print("\nCache Hit!")
                            print(f"Block Number - {int(address[ : address_bits - word_bits], 2)}")
                            print(f"Cache Line - {i}")
                            Words = CacheMemory["C" + str(i)]
                            W = ""
                            found = True

                            for i in range(words_per_block):
                                W += Words[0][i][0] + " "

                            print("Words - " + W)
                            break

                if found is False:
                    print("\nCache Miss!\nCould not find the requested word.")
            # Exit
            elif c == "3":
                print("\nEnded Successfully!")
                break
            # Wrong Selection
            else:
                print("Only choose among the provided options!")
    # N - Way Set Associative Mapping
    elif c == "3":
        n = int(input("\nEnter the value of N - "))
        set_bits = len(bin(n - 1).replace("0b", ""))
        print("\nAddress Bits - " + str(address_bits))
        print("Words Bits - " + str(word_bits))
        print("Set Bits - " + str(set_bits))
        print("Tag Bits - " + str(address_bits - word_bits - set_bits))
        tag_bits = address_bits - word_bits - set_bits
        Counters = [0 for x in range(n)]

        while(True):
            c = input("\n>> 1 << Load a word into cache memory \n>> 2 << Search cache memory \n>> 3 << Exit \n\nChoice - ")

            # Loading
            if c == "1":
                address = input("\nEnter the address - ")
                word = int(address[-word_bits : ], 2)
                set_number = int(address[tag_bits : tag_bits + set_bits], 2)
                tag = address[ : tag_bits]
                block_number = int(address[ : address_bits - word_bits], 2)
                temp = cache_lines // n

                if CacheMemory["C" + str(temp * set_number + Counters[set_number])] == [None, None]:
                    CacheMemory["C" + str(temp * set_number + Counters[set_number])] = [MainMemory["B" + str(block_number)], address]   # Adding a copy of block to the cache line
                else:
                    print("\nBlock Replacement! Address " + CacheMemory["C" + str(temp * set_number + Counters[set_number])][1] + " will be replaced by " + address + ".")
                    CacheMemory["C" + str(temp * set_number + Counters[set_number])] = [MainMemory["B" + str(block_number)], address]   # Adding a copy of block to the cache line

                Counters[set_number] += 1

                # FIFO Replacement Policy
                if Counters[set_number] == temp:
                    Counters[set_number] = 0
            # Searching
            elif c == "2":
                address = input("\nEnter the address - ")
                set_number = int(address[tag_bits : tag_bits + set_bits], 2)
                tag = address[ : tag_bits]
                temp = cache_lines // n
                found = False

                # Iterating over the set
                for i in range(temp * set_number, temp * set_number + temp):
                    if CacheMemory["C" + str(i)] != [None, None]:
                        if CacheMemory["C" + str(i)][1] == address:
                            print("\nCache Hit!")
                            print(f"Block Number - {int(address[ : address_bits - word_bits], 2)}")
                            print(f"Set Number - {set_number}")
                            Words = CacheMemory["C" + str(i)]
                            W = ""

                            for i in range(words_per_block):
                                W += Words[0][i][0] + " "

                            print("Words - " + W)
                            found = True
                            break
                    else:
                        break

                if found is False:
                    print("\nCache Miss!\nRequested word is missing.")
            # Exit
            elif c == "3":
                print("\nEnded Successfully!")
                break
            # Wrong Selection
            else:
                print("Only choose among the provided options!")
# Multilevel Cache Memory
elif mode == "2":
    size_main = int(input("Enter the size of Main Memory - "))                                # Main Memory Size
    size_cache_two = int(input("Enter the size of Level 2 Cache Memory - "))                  # Level 2 Cache Size
    size_cache_one = size_cache_two // 2                                                      # Level 1 Cache Size
    words_per_block = int(input("Enter the number of words in each block - "))
    cache_lines_one = size_cache_one // words_per_block                                       # Cache Lines in Level 1 Cache
    cache_lines_two = size_cache_two // words_per_block                                       # Cache Lines in Level 2 Cache
    blocks = size_main // words_per_block
    address_bits = int(math.log(size_main, 2))

    MainMemory = {}

    for i, j in zip(range(0, size_main, words_per_block), range(blocks)):
        MainMemory["B" + str(j)] = []
        for x in range(words_per_block):
            # Contents - Word + Number String, Address, Block Number, Place within the Block, Word Number
            MainMemory["B" + str(j)].append(["W" + str(i + x), bin(i + x).replace("0b", "").rjust(address_bits, "0"), j, x, i + x])

    CacheMemoryOne = {}                 # Level 1 Cache Memory

    for j in range(cache_lines_one):
        # Contents - Block, Address
        CacheMemoryOne["C" + str(j)] = [None, None]

    CacheMemoryTwo = {}                 # Level 2 Cache Memory

    for j in range(cache_lines_two):
        # Contents - Block, Address
        CacheMemoryOne["C" + str(j)] = [None, None]


    word_bits = len(bin(words_per_block - 1).replace("0b", ""))
    cl_bits_one = len(bin(cache_lines_one - 1).replace("0b", ""))        # Bits for cache lines in Level 1 Cache
    cl_bits_two = len(bin(cache_lines_two - 1).replace("0b", ""))        # Bits for cache lines in Level 2 Cache
    tag_bits_one = address_bits - word_bits - cl_bits_one                # Bits for tags in Level 1 Cache
    tag_bits_two = address_bits - word_bits - cl_bits_two                # Bits for tags in Level 2 Cache

    c = input("\n>> 1 << Direct Mapping \n>> 2 << Associative Memory \n>> 3 << N - Way Set Associative Memory \n\nChoice - ")

    # Direct Mapping
    if c == "1":
        print("\nAddress Bits - " + str(address_bits))
        print("Words Bits - " + str(word_bits))
        print("Level One Cache Line Bits - " + str(cl_bits_one))
        print("Level Two Cache Line Bits - " + str(cl_bits_two))
        print("Level One Tag Bits - " + str(tag_bits_one))
        print("Level Two Tag Bits - " + str(tag_bits_two))

        while(True):
            c = input("\n>> 1 << Load a word into cache memory \n>> 2 << Search cache memory \n>> 3 << Exit \n\nChoice - ")

            # Loading
            if c == "1":
                address = input("\nEnter the address - ")
                word = int(address[-word_bits : ], 2)
                cache_line = int(address[tag_bits_one : tag_bits_one + cl_bits_one], 2)
                tag = address[ : tag_bits_one]
                block_number = int(address[ : tag_bits_one + cl_bits_one], 2)

                if CacheMemoryOne["C" + str(cache_line)] == [None, None]:
                    CacheMemoryOne["C" + str(cache_line)] = [MainMemory["B" + str(block_number)], address]   # Adding a copy of block to the cache line
                # Transferring the removed elements of Level 1 Cache to Level 2 Cache
                else:
                    print("\nBlock Replacement! Address " + CacheMemoryOne["C" + str(cache_line)][1] + " will be replaced by " + address + ".")
                    X = CacheMemoryOne["C" + str(cache_line)]
                    CacheMemoryOne["C" + str(cache_line)] = [MainMemory["B" + str(block_number)], address]   # Adding a copy of block to the cache line
                    cache_line_two = int(X[1][tag_bits_two : tag_bits_two + cl_bits_two], 2)
                    CacheMemoryTwo["C" + str(cache_line_two)] = X
            # Searching
            elif c == "2":
                address = input("\nEnter the address - ")
                cache_line = int(address[tag_bits_one : tag_bits_one + cl_bits_one], 2)
                tag = address[ : tag_bits_one]
                found = False

                if CacheMemoryOne["C" + str(cache_line)] != [None, None]:
                    # Searching Level 1 Cache
                    if CacheMemoryOne["C" + str(cache_line)][1] == address:
                        print("\nCache Hit!")
                        print(f"Block Number - {int(address[ : tag_bits_one + cl_bits_one], 2)}")
                        print(f"Cache Line - {cache_line}")
                        print("Cache Level - 1")
                        Words = CacheMemoryOne["C" + str(cache_line)]
                        W = ""

                        for i in range(words_per_block):
                            W += Words[0][i][0] + " "

                        print("Words - " + W)
                        found = True
                    # Searching Level 2 Cache
                    elif found is False:
                        cache_line_two = int(address[tag_bits_two : tag_bits_two + cl_bits_two], 2)

                        if CacheMemoryTwo["C" + str(cache_line_two)][1] == address:
                            print("\nCache Hit!")
                            print(f"Block Number - {int(address[ : tag_bits_two + cl_bits_two], 2)}")
                            print(f"Cache Line - {cache_line_two}")
                            print("Cache Level - 2")
                            Words = CacheMemoryTwo["C" + str(cache_line_two)]
                            W = ""

                            for i in range(words_per_block):
                                W += Words[0][i][0] + " "

                            print("Words - " + W)
                            found = True

                    if found is False:
                        print("Cache Miss! Requested Address is missing.")

                else:
                    print("Cache Miss! Requested Address is missing.")
            # Exit
            elif c == "3":
                print("\nEnded Successfully!")
                break
            # Wrong Selection
            else:
                print("Only choose among the provided options!")
    # Associative Mapping
    elif c == "2":
        print("\nAddress Bits - " + str(address_bits))
        print("Words Bits - " + str(word_bits))
        print("Tag Bits - " + str(address_bits - word_bits))
        counter_one = 0          # Level 1 Counter
        counter_two = 0          # Level 2 Counter

        while (True):
            c = input("\n>> 1 << Load a word into cache memory \n>> 2 << Search cache memory \n>> 3 << Exit \n\nChoice - ")

            # Loading
            if c == "1":
                address = input("\nEnter the address - ")
                word = int(address[-word_bits : ], 2)
                tag = address[ : address_bits - word_bits]
                block_number = int(address[ : address_bits - word_bits], 2)

                if CacheMemoryOne["C" + str(counter_one)] == [None, None]:
                    CacheMemoryOne["C" + str(counter_one)] = [MainMemory["B" + str(block_number)], address]   # Adding a copy of block to the cache line
                else:
                    print("\nBlock Replacement! Address " + CacheMemoryOne["C" + str(counter_one)][1] + " will be replaced by " + address + ".")
                    X = CacheMemoryOne["C" + str(counter_one)]
                    CacheMemoryOne["C" + str(counter_one)] = [MainMemory["B" + str(block_number)], address]   # Adding a copy of block to the cache line
                    CacheMemoryTwo["C" + str(counter_two)] = X
                    counter_two += 1

                    # FIFO Replacement Policy
                    if counter_two == cache_lines_two:
                        counter_two = 0

                counter_one += 1

                # FIFO replacement policy
                if counter_one == cache_lines_one:
                    counter_one = 0
            # Searching
            elif c == "2":
                address = input("\nEnter the address - ")
                tag = address[ : address_bits - word_bits]
                found = False

                # Searching Level 1 Cache
                for i in range(cache_lines_one):
                    if CacheMemoryOne["C" + str(i)] != [None, None]:
                        if CacheMemoryOne["C" + str(i)][1] == address:
                            print("\nCache Hit!")
                            print(f"Block Number - {int(address[ : address_bits - word_bits], 2)}")
                            print(f"Cache Line - {i}")
                            print("Cache Level - 1")
                            Words = CacheMemoryOne["C" + str(i)]
                            W = ""
                            found = True

                            for i in range(words_per_block):
                                W += Words[0][i][0] + " "

                            print("Words - " + W)
                            break
                    else:
                        break
                # Searching Level 2 Cache
                if found is False:
                    for i in range(cache_lines_two):
                        if CacheMemoryTwo["C" + str(i)] != [None, None]:
                            if CacheMemoryTwo["C" + str(i)][1] == address:
                                print("\nCache Hit!")
                                print(f"Block Number - {int(address[ : address_bits - word_bits], 2)}")
                                print(f"Cache Line - {i}")
                                print("Cache Level - 2")
                                Words = CacheMemoryTwo["C" + str(i)]
                                W = ""
                                found = True

                                for i in range(words_per_block):
                                    W += Words[0][i][0] + " "

                                print("Words - " + W)
                                break
                        else:
                            break

                if found is False:
                    print("\nCache Miss!\nRequested word missing.")
            # Exit
            elif c == "3":
                print("\nEnded Successfully!")
                break
            # Wrong Selection
            else:
                print("Only choose among the provided options!")
    # N - Way Set Associative Mapping
    elif c == "3":
        n = int(input("\nEnter the value of N - "))
        set_bits = len(bin(n - 1).replace("0b", ""))
        print("\nAddress Bits - " + str(address_bits))
        print("Words Bits - " + str(word_bits))
        print("Set Bits - " + str(set_bits))
        print("Tag Bits - " + str(address_bits - word_bits - set_bits))
        tag_bits = address_bits - word_bits - set_bits
        CountersOne = [0 for x in range(n)]
        CountersTwo = [0 for x in range(n)]

        while(True):
            c = input("\n>> 1 << Load a word into cache memory \n>> 2 << Search cache memory \n>> 3 << Exit \n\nChoice - ")

            # Loading
            if c == "1":
                address = input("\nEnter the address - ")
                word = int(address[-word_bits : ], 2)
                set_number = int(address[tag_bits : tag_bits + set_bits], 2)
                tag = address[ : tag_bits]
                block_number = int(address[ : address_bits - word_bits], 2)
                temp_one = cache_lines_one // n
                temp_two = cache_lines_two // n

                if CacheMemoryOne["C" + str(temp_one * set_number + CountersOne[set_number])] == [None, None]:
                    CacheMemoryOne["C" + str(temp_one * set_number + CountersOne[set_number])] = [MainMemory["B" + str(block_number)], address]   # Adding a copy of block to the cache line
                else:
                    print("\nBlock Replacement! Address " + CacheMemoryOne["C" + str(temp_one * set_number + CountersOne[set_number])][1] + " will be replaced by " + address + ".")
                    X = CacheMemoryOne["C" + str(temp_one * set_number + CountersOne[set_number])]
                    CacheMemoryOne["C" + str(temp_one * set_number + CountersOne[set_number])] = [MainMemory["B" + str(block_number)], address]   # Adding a copy of block to the cache line
                    CacheMemoryTwo["C" + str(temp_two * set_number + CountersTwo[set_number])] = X
                    CountersTwo[set_number] += 1

                    # FIFO Replacement Policy
                    if CountersTwo[set_number] == temp_two:
                        CountersTwo[set_number] = 0

                CountersOne[set_number] += 1

                # FIFO Replacement Policy
                if CountersOne[set_number] == temp_one:
                    CountersOne[set_number] = 0
            # Searching
            elif c == "2":
                address = input("\nEnter the address - ")
                set_number = int(address[tag_bits : tag_bits + set_bits], 2)
                tag = address[ : tag_bits]
                temp_one = cache_lines_one // n
                temp_two = cache_lines_two // n
                found = False

                # Searching Level 1 Cache
                for i in range(temp_one * set_number, temp_one * set_number + temp_one):
                    if CacheMemoryOne["C" + str(i)] != [None, None]:
                        if CacheMemoryOne["C" + str(i)][1] == address:
                            print("\nCache Hit!")
                            print(f"Block Number - {int(address[ : address_bits - word_bits], 2)}")
                            print(f"Set Number - {set_number}")
                            print("Cache Level - 1")
                            Words = CacheMemoryOne["C" + str(i)]
                            W = ""

                            for i in range(words_per_block):
                                W += Words[0][i][0] + " "

                            print("Words - " + W)
                            found = True
                            break
                    else:
                        break

                # Searching Level 2 Cache
                if found is False:
                    for i in range(temp_two * set_number, temp_two * set_number + temp_two):
                        if CacheMemoryTwo["C" + str(i)] != [None, None]:
                            if CacheMemoryTwo["C" + str(i)][1] == address:
                                print("\nCache Hit!")
                                print(f"Block Number - {int(address[ : address_bits - word_bits], 2)}")
                                print(f"Set Number - {set_number}")
                                print("Cache Level - 2")
                                Words = CacheMemoryTwo["C" + str(i)]
                                W = ""

                                for i in range(words_per_block):
                                    W += Words[0][i][0] + " "

                                print("Words - " + W)
                                found = True
                                break
                        else:
                            break

                if found is False:
                    print("\nCache Miss!\nRequested word is missing.")
            # Exit
            elif c == "3":
                print("\nEnded Successfully!")
                break
            # Wrong Selection
            else:
                print("Only choose among the provided options!")
else:
    print("Only choose among the provided modes!")

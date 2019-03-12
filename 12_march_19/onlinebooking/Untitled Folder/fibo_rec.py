def gen_seq(length):
    if(length <= 1):
        return length
    else:
        return (gen_seq(length-1) + gen_seq(length-2))

length = int(input("Enter number of terms:"))

print("Fibonacci sequence using Recursion :")
for iter in range(length):
    print(gen_seq(iter))

def file_read(file_name):
    with open(file_name, 'r') as w:
        w.read()
        if 'fdr1' in w:
            return file_name
        else:
            return file_read(file_name)


file_open = file_read(file_name)
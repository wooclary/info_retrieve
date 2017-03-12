from ir.gen_record import gen, fm

file_names = fm.get_filename_list()
for fname in file_names:
    print(fname + ':')
    records = gen(fname, fname, from_file=True)
    for record in records:
        print(record)
    print('##############')

# fname = ''
# records = gen(fname, fname, from_file=True)
# for record in records:
#     print(record)
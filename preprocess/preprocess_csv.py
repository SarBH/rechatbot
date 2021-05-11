import csv


def read_contexts_to_list(context_path):
    contexts = {}
    with open(context_path) as context_file:
        csv_reader = csv.reader(context_file, delimiter='\t')
        line_count = 0

        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                contexts[row[0]] = row[1]
                line_count += 1
        
        print(f'Processed {line_count} lines.')
    return contexts




def read_data_to_dict(questions_path, contexts_dict, destination_path):
    data = {}

    with open(destination_path, 'w', newline='') as csvfile:
        questions_writer = csv.writer(csvfile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)


        with open(questions_path) as questions_file:
            csv_reader = csv.reader(questions_file, delimiter='\t')
            line_count = 0

            seen_titles = set()

            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    qas = {}
                    title, question, text, ans_start, is_impossible = row
                    if title not in seen_titles:
                        id_counter = 0
                        seen_titles.add(title)
                    else: id_counter += 1

                    if text != '':
                        ans_start = contexts_dict[title].find(text)
                    else:
                        continue
                    # if text2 != '':
                    #     ans_start2 = contexts_dict[title].find(text)

                    id = str(title + str(id_counter))
                    questions_writer.writerow([id, title, contexts_dict[title], question, ans_start, text])
                    



if __name__ == "__main__":
    contexts = read_contexts_to_list("preprocess/Questions and contexts - context.tsv")
    data = read_data_to_dict("preprocess/Questions and contexts - data.tsv", contexts, "preprocess/questions_complete.tsv")
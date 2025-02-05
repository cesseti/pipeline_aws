rdd = sc.textFile("/home/jovyan/README.md")

words = rdd.flatMap(lambda line: line.split())

word_counts = words.map(lambda word: (word, 1))

word_counts = word_counts.reduceByKey(lambda a, b: a + b)

word_counts.collect()

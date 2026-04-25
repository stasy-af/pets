import math

m, n, k = map(int, input().split())
training_letters = []
testing_letters = []
for _ in range(m):
    training_letters.append(list(map(int, input().split())))
for _ in range(n):
    testing_letters.append(list(map(int, input().split())))
cSpam, cNotSpam = 0, 0
for row in training_letters:
    if row[0] == 1:
        cSpam += 1
    elif row[0] == 0:
        cNotSpam += 1
if cSpam == 0 or cNotSpam == 0:
    pSpam = (cSpam + 1) / (m + 2)
    pNotSpam = (cNotSpam + 1) / (m + 2)
else:
    pSpam = cSpam / m
    pNotSpam = cNotSpam / m
    
keywords = {}
for i in range(1, k + 1):
    keywords[i] = [[], []]

for row in training_letters:
    label = row[0]
    for j in range(1, k + 1):
        if label == 1:
            keywords[j][0].append(row[j])
        else:
            keywords[j][1].append(row[j])

alpha = 0.25  
for key in keywords:
    if cSpam > 0:
        spam_count = sum(keywords[key][0])
        keywords[key][0] = (spam_count + alpha) / (cSpam + 2 * alpha)
    else:
        keywords[key][0] = 0.5

    if cNotSpam > 0:
        not_spam_count = sum(keywords[key][1])
        keywords[key][1] = (not_spam_count + alpha) / (cNotSpam + 2 * alpha)
    else:
        keywords[key][1] = 0.5

result = []
UNCERTAINTY_THRESHOLD = 0.01  

for test in testing_letters:
    log_spam_prob = math.log(pSpam)
    log_not_spam_prob = math.log(pNotSpam)

    for index in range(k):
        if test[index] == 1:
            log_spam_prob += math.log(keywords[index + 1][0])
            log_not_spam_prob += math.log(keywords[index + 1][1])
        else:
            log_spam_prob += math.log(1 - keywords[index + 1][0])
            log_not_spam_prob += math.log(1 - keywords[index + 1][1])
    log_diff = abs(log_spam_prob - log_not_spam_prob)
    if log_diff < UNCERTAINTY_THRESHOLD:
        result.append(-1)
    elif log_spam_prob > log_not_spam_prob:
        result.append(1)
    else:
        result.append(0)

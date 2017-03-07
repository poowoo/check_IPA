# -*- coding: utf8 -*-
import sys
import os

#check contant all ipa
#Usage: filename log


def add_phone_to_dict(phones,input_ipa):

	for phone in phones:
		if phone in input_ipa:			
			input_ipa[phone] += 1 
		else:
			input_ipa[phone] = 1

def add_input_ipa(toks,input_ipa):

	for tok in toks:
		if tok.find(".") == -1:
			phones = tok.split("-")
			add_phone_to_dict(phones,input_ipa)
		else:			
			syls = tok.split(".")
			for syl in syls:
				phones = syl.split("-")
				add_phone_to_dict(phones,input_ipa)
		
def cmp_input_ipa(toks,input_ipa):

	tmp_dict = {}
	phone_count = 0
	cnt = 0
	for tok in toks:
		if tok.find(".") == -1:
			phones = tok.split("-")
			phone_count += len(phones)
			add_phone_to_dict(phones,tmp_dict)
		else:			
			syls = tok.split(".")
			for syl in syls:
				phones = syl.split("-")
				phone_count += len(phones)
				add_phone_to_dict(phones,tmp_dict)
	for phone in tmp_dict:
		if input_ipa[phone] < 2:
			return -1.0
		else:
			cnt += input_ipa[phone] - tmp_dict[phone]
	return cnt/phone_count

def find_max(scores):

	max_tmp = 0
	index = -1
	j = 0
	for num in scores:
		if max_tmp < num:
			max_tmp = num
			index = j
		j += 1
	return index

if __name__ == '__main__':	

	scores = []
	out = open(sys.argv[2], mode='w', encoding='UTF-8')
	with open(sys.argv[1], mode='r', encoding='UTF-8') as file:
		
		input_ipa = {}
		lines = file.readlines()
		text = []
		i = 0
		add_dict = 0
		while i < len(lines):
			line = lines[i].strip()	
			toks = line.split("\t")
			text.append(toks[0].replace("|", ""))			
			toks[1] = [x for x in toks[1].split("|") if x != '']
			if add_dict == 0:
				add_input_ipa(toks[1],input_ipa)			
			else:
				score = cmp_input_ipa(toks[1],input_ipa)
				out.write(text[i]+":"+str(round(score,2))+"\n")
				scores.append(score)
			i += 1
			if i == len(lines):
				add_dict += 1
				i = 0
			if add_dict > 1:
				out.write("Max score sentens\n")
				max_num = 0				
				while max_num < 3:
					index = find_max(scores)
					out.write(text[index]+"\t:\t"+str(round(scores[index],2))+"\n")
					scores[index] = 0
					max_num += 1
				out.close()
				break



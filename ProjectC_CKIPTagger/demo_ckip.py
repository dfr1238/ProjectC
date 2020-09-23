from ckiptagger import WS, POS, NER #導入CKIPTAGGER

ckip_Data="/home/dfr1238/CKIPtagger_data/data" #訓練資料路徑
ws = WS(ckip_Data) #指定到訓練資料
pos = POS(ckip_Data) #指定到訓練資料
ner = NER(ckip_Data) #指定到訓練資料

sentence_list = ["傅達仁今將執行安樂死，卻突然爆出自己20年前遭緯來體育台封殺，他不懂自己哪裡得罪到電視台。",
"美國參議院針對今天總統布什所提名的勞工部長趙小蘭展開認可聽 證會，預料她將會很順利通過參議院支持，成為該國有史以來第一位的華裔女性內閣成員。",
"","土地公有政策?？還是土地婆有政策。.","… 你確定嗎… 不要再騙了……",
"最多容納59,000個人,或5.9萬人,再多就不行了.這是環評的結論.",
"科長說:1,坪數對人數為1:3。2,可以再增加。"]

word_s = ws(sentence_list,
            sentence_segmentation=True,
            segment_delimiter_set={'?', '？', '!', '！', '。', ',','，', ';', ':', '、'})

print(word_s)
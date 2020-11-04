# -*- coding: UTF-8 -*-
import tensorflow as tf
from ckiptagger import WS, POS, NER #導入CKIPTAGGER


ckip_Data="D:\CKIPtagger_data\data" #訓練資料路徑
ws = WS(ckip_Data, disable_cuda=False) #指定到訓練資料
pos = POS(ckip_Data, disable_cuda=False) #指定到訓練資料
ner = NER(ckip_Data, disable_cuda=False) #指定到訓練資料

sentence_list = ["美國政府今天證實，會修改美國企業和中國華為公司商業往來的相關禁令，允許美企和華為合作制定5G標準。路透社引述消息人士報導，這項法規修改獲美國商務部等部門通過，12日已提交聯邦公報（Federal Register），最快16日公布。美國商務部長羅斯（Wilbur Ross）發聲明證實這項舉措：「美國不會放棄在全球創新領域的領導地位，（商務部）會致力保護美國的國家安全和外交政策利益，鼓勵美國產業全面參與和提倡美國技術成為國際標準。」美國商務部今天稍後也公開宣布，美國參與標準制定「會影響5G、自動駕駛汽車、人工智慧和其他尖端技術的未來」。華為暫未對此事發表評論。美國去年將華為列入出口管制實體清單（entity list），以國家安全為由，禁止華為在未經政府許可下，向美國企業採購零組件和技術。產業人士和政府官員表示，此舉不該被解讀為美國對全球最大電信設備製造商華為立場軟化。他們表示，華為被列入實體清單，不利美國參與標準的制定，因為美企無法確定哪些資訊可分享，美國工程師在制定標準的會議中不出聲，反會讓華為取得更大的發言權。資訊科技業協會（Information Technology Industry Council）亞洲政策高階主任威爾遜（Naomi Wilson）說：「2019年5月實體清單的更新引發混亂，無意中使美國公司被排除在一些技術標準對話之外，使美企處於劣勢。」資訊科技業協會所代表的企業包含亞馬遜（Amazon.com Inc）、高通（Qualcomm Inc）和英特爾（Intel Corp.）等大廠。日經亞洲評論（Nikkei Asian Review）指出，華為在5G標準制定上，近年已躍居全球領導者地位。德國的專利統計公司IPlytics一份研究指出，華為在5G標準的研發上排名世界第一，提出的相關專利截至今年1月便有3147項，三星（Samsung）、中興通訊（ZTE）與樂金電子（LG Electronics）分居第2到第4。設於波士頓的顧問企業「策略分析公司」（Strategy Analytics）也有一份類似研究。在分析國際電訊標準訂定組織「第三代合作夥伴計畫」（3GPP）的600個會員企業後，發現華為在制定5G標準的貢獻度上執世界牛耳。日經亞洲評論認為，美國去年5月所頒的華為禁令阻止美企與華為的技術合作，當時就有許多政府官員與科技業者警告，這會傷害到美國參與全球5G標準的制定。"]

word_s = ws(sentence_list,
            sentence_segmentation=True,
            segment_delimiter_set={'?', '？', '!', '！', '。', ',','，', ';', ':', '、'})

print(word_s)
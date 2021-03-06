import datetime

from samo.core import db
from samo.models import User, Post, Tag, Comment, Role

# data from http://www.lipsum.com

DUMMY_CONTENT = [{'comm_content': 'My opinion.',
                  'content': 'Where does it come from?\nContrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of "de Finibus Bonorum et Malorum" (The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, "Lorem ipsum dolor sit amet..", comes from a line in section 1.10.32.\n\nThe standard chunk of Lorem Ipsum used since the 1500s is reproduced below for those interested. Sections 1.10.32 and 1.10.33 from "de Finibus Bonorum et Malorum" by Cicero are also reproduced in their exact original form, accompanied by English versions from the 1914 translation by H. Rackham. ',
                  'lang_name': 'English',
                  'name': 'John',
                  'title': 'This is a test'},
                 {'comm_content': 'Моё мнение.',
                  'content': 'Откуда он появился?\nМногие думают, что Lorem Ipsum - взятый с потолка псевдо-латинский набор слов, но это не совсем так. Его корни уходят в один фрагмент классической латыни 45 года н.э., то есть более двух тысячелетий назад. Ричард МакКлинток, профессор латыни из колледжа Hampden-Sydney, штат Вирджиния, взял одно из самых странных слов в Lorem Ipsum, "consectetur", и занялся его поисками в классической латинской литературе. В результате он нашёл неоспоримый первоисточник Lorem Ipsum в разделах 1.10.32 и 1.10.33 книги "de Finibus Bonorum et Malorum" ("О пределах добра и зла"), написанной Цицероном в 45 году н.э. Этот трактат по теории этики был очень популярен в эпоху Возрождения. Первая строка Lorem Ipsum, "Lorem ipsum dolor sit amet..", происходит от одной из строк в разделе 1.10.32\n\nКлассический текст Lorem Ipsum, используемый с XVI века, приведён ниже. Также даны разделы 1.10.32 и 1.10.33 "de Finibus Bonorum et Malorum" Цицерона и их английский перевод, сделанный H. Rackham, 1914 год.',
                  'lang_name': 'Russian',
                  'name': 'Иван',
                  'title': 'Это тест'},
                 {'comm_content': 'Meine Meinung.',
                  'content': 'Wo kommt es her?\nGlauben oder nicht glauben, Lorem Ipsum ist nicht nur ein zufälliger Text. Er hat Wurzeln aus der Lateinischen Literatur von 45 v. Chr, was ihn über 2000 Jahre alt macht. Richar McClintock, ein Lateinprofessor des Hampden-Sydney College in Virgnia untersuche einige undeutliche Worte, "consectetur", einer Lorem Ipsum Passage und fand eine unwiederlegbare Quelle. Lorem Ipsum komm aus der Sektion 1.10.32 und 1.10.33 des "de Finibus Bonorum et Malorum" (Die Extreme von Gut und Böse) von Cicero, geschrieben 45 v. Chr. Dieses Buch ist Abhandlung der Ethiktheorien, sehr bekannt wärend der Renaissance. Die erste Zeile des Lorem Ipsum, "Lorem ipsum dolor sit amet...", kommt aus einer Zeile der Sektion 1.10.32.\n\nDer Standardteil von Lorem Ipsum, genutzt seit 1500, ist reproduziert für die, die es interessiert. Sektion 1.10.32 und 1.10.33 von "de Finibus Bonorum et Malroum" von Cicero sind auch reproduziert in ihrer Originalform, abgeleitet von der Englischen Version aus von 1914 (H. Rackham)',
                  'lang_name': 'German',
                  'name': 'Johann',
                  'title': 'Das ist ein Test'},
                 {'comm_content': 'Mоя думка.',
                  'content': 'Звідки він походить?\nНа відміну від поширеної думки Lorem Ipsum не є випадковим набором літер. Він походить з уривку класичної латинської літератури 45 року до н.е., тобто має більш як 2000-річну історію. Річард Макклінток, професор латини з коледжу Хемпдін-Сидні, що у Вірджінії, вивчав одне з найменш зрозумілих латинських слів - consectetur - з уривку Lorem Ipsum, і у пошуку цього слова в класичній літературі знайшов безсумнівне джерело. Lorem Ipsum походить з розділів 1.10.32 та 1.10.33 цицеронівського "de Finibus Bonorum et Malorum" ("Про межі добра і зла"), написаного у 45 році до н.е. Цей трактат з теорії етики був дуже популярним в епоху Відродження. Перший рядок Lorem Ipsum, "Lorem ipsum dolor sit amet..." походить з одного з рядків розділу 1.10.32.\n\nКласичний текст, використовуваний з XVI сторіччя, наведено нижче для всіх зацікавлених. Також точно за оригіналом наведено розділи 1.10.32 та 1.10.33 цицеронівського "de Finibus Bonorum et Malorum" разом із перекладом англійською, виконаним 1914 року Х.Рекемом. ',
                  'lang_name': 'Ukrainian',
                  'name': 'Iван',
                  'title': 'Це приклад.'},
                 {'comm_content': 'Parerea mea.',
                  'content': ' De unde provine?\nÎn ciuda opiniei publice, Lorem Ipsum nu e un simplu text fără sens. El îşi are rădăcinile într-o bucată a literaturii clasice latine din anul 45 î.e.n., făcând-o să aibă mai bine de 2000 ani. Profesorul universitar de latină de la colegiul Hampden-Sydney din Virginia, Richard McClintock, a căutat în bibliografie unul din cele mai rar folosite cuvinte latine "consectetur", întâlnit în pasajul Lorem Ipsum, şi căutând citate ale cuvântului respectiv în literatura clasică, a descoperit la modul cel mai sigur sursa provenienţei textului. Lorem Ipsum provine din secţiunile 1.10.32 şi 1.10.33 din "de Finibus Bonorum et Malorum" (Extremele Binelui şi ale Răului) de Cicerone, scrisă în anul 45 î.e.n. Această carte este un tratat în teoria eticii care a fost foarte popular în perioada Renasterii. Primul rând din Lorem Ipsum, "Lorem ipsum dolor sit amet...", a fost luat dintr-un rând din secţiunea 1.10.32.\n\nPasajul standard de Lorem Ipsum folosit încă din secolul al XVI-lea este reprodus mai jos pentru cei interesaţi. Secţiunile 1.10.32 şi 1.10.33 din "de Finibus Bonorum et Malorum" de Cicerone sunt de asemenea reproduse în forma lor originală, impreună cu versiunile lor în engleză din traducerea de către H. Rackham din 1914',
                  'lang_name': 'Romanian',
                  'name': 'Ion',
                  'title': 'Acesta este un test'},
                 {'comm_content': 'Mon opinion.',
                  'content': 'D\'où vient-il?\nContrairement à une opinion répandue, le Lorem Ipsum n\'est pas simplement du texte aléatoire. Il trouve ses racines dans une oeuvre de la littérature latine classique datant de 45 av. J.-C., le rendant vieux de 2000 ans. Un professeur du Hampden-Sydney College, en Virginie, s\'est intéressé à un des mots latins les plus obscurs, consectetur, extrait d\'un passage du Lorem Ipsum, et en étudiant tous les usages de ce mot dans la littérature classique, découvrit la source incontestable du Lorem Ipsum. Il provient en fait des sections 1.10.32 et 1.10.33 du "De Finibus Bonorum et Malorum" (Des Suprêmes Biens et des Suprêmes Maux) de Cicéron. Cet ouvrage, très populaire pendant la Renaissance, est un traité sur la théorie de l\'éthique. Les premières lignes du Lorem Ipsum, "Lorem ipsum dolor sit amet...", proviennent de la section 1.10.32.\n\nL\'extrait standard de Lorem Ipsum utilisé depuis le XVIè siècle est reproduit ci-dessous pour les curieux. Les sections 1.10.32 et 1.10.33 du "De Finibus Bonorum et Malorum" de Cicéron sont aussi reproduites dans leur version originale, accompagnée de la traduction anglaise de H. Rackham (1914). ',
                  'lang_name': 'French',
                  'name': 'Jean',
                  'title': "C'est un test"},
                 {'comm_content': 'Moja opinia.',
                  'content': 'Skąd się to wzięło?\nW przeciwieństwie do rozpowszechnionych opinii, Lorem Ipsum nie jest tylko przypadkowym tekstem. Ma ono korzenie w klasycznej łacińskiej literaturze z 45 roku przed Chrystusem, czyli ponad 2000 lat temu! Richard McClintock, wykładowca łaciny na uniwersytecie Hampden-Sydney w Virginii, przyjrzał się uważniej jednemu z najbardziej niejasnych słów w Lorem Ipsum – consectetur – i po wielu poszukiwaniach odnalazł niezaprzeczalne źródło: Lorem Ipsum pochodzi z fragmentów (1.10.32 i 1.10.33) „de Finibus Bonorum et Malorum”, czyli „O granicy dobra i zła”, napisanej właśnie w 45 p.n.e. przez Cycerona. Jest to bardzo popularna w czasach renesansu rozprawa na temat etyki. Pierwszy wiersz Lorem Ipsum, „Lorem ipsum dolor sit amet...” pochodzi właśnie z sekcji 1.10.32.\n\nStandardowy blok Lorem Ipsum, używany od XV wieku, jest odtworzony niżej dla zainteresowanych. Fragmenty 1.10.32 i 1.10.33 z „de Finibus Bonorum et Malorum” Cycerona, są odtworzone w dokładnej, oryginalnej formie, wraz z angielskimi tłumaczeniami H. Rackhama z 1914 roku.',
                  'lang_name': 'Polish',
                  'name': 'Janek',
                  'title': 'To jest test'},
                 {'comm_content': 'Y kiến của tôi.',
                  'content': 'Nó đến từ đâu?\nTrái với quan điểm chung của số đông, Lorem Ipsum không phải chỉ là một đoạn văn bản ngẫu nhiên. Người ta tìm thấy nguồn gốc của nó từ những tác phẩm văn học la-tinh cổ điển xuất hiện từ năm 45 trước Công Nguyên, nghĩa là nó đã có khoảng hơn 2000 tuổi. Một giáo sư của trường Hampden-Sydney College (bang Virginia - Mỹ) quan tâm tới một trong những từ la-tinh khó hiểu nhất, "consectetur", trích từ một đoạn của Lorem Ipsum, và đã nghiên cứu tất cả các ứng dụng của từ này trong văn học cổ điển, để từ đó tìm ra nguồn gốc không thể chối cãi của Lorem Ipsum. Thật ra, nó được tìm thấy trong các đoạn 1.10.32 và 1.10.33 của "De Finibus Bonorum et Malorum" (Đỉnh tối thượng của Cái Tốt và Cái Xấu) viết bởi Cicero vào năm 45 trước Công Nguyên. Cuốn sách này là một luận thuyết đạo lí rất phổ biến trong thời kì Phục Hưng. Dòng đầu tiên của Lorem Ipsum, "Lorem ipsum dolor sit amet..." được trích từ một câu trong đoạn thứ 1.10.32.\n\nTrích đoạn chuẩn của Lorem Ipsum được sử dụng từ thế kỉ thứ 16 và được tái bản sau đó cho những người quan tâm đến nó. Đoạn 1.10.32 và 1.10.33 trong cuốn "De Finibus Bonorum et Malorum" của Cicero cũng được tái bản lại theo đúng cấu trúc gốc, kèm theo phiên bản tiếng Anh được dịch bởi H. Rackham vào năm 1914.',
                  'lang_name': 'Vietnamese',
                  'name': 'Tuan',
                  'title': 'đây là một bài kiểm tra'},
                 {'comm_content': 'Mia opinione.',
                  'content': 'Da dove viene?\nAl contrario di quanto si pensi, Lorem Ipsum non è semplicemente una sequenza casuale di caratteri. Risale ad un classico della letteratura latina del 45 AC, cosa che lo rende vecchio di 2000 anni. Richard McClintock, professore di latino al Hampden-Sydney College in Virginia, ha ricercato una delle più oscure parole latine, consectetur, da un passaggio del Lorem Ipsum e ha scoperto tra i vari testi in cui è citata, la fonte da cui è tratto il testo, le sezioni 1.10.32 and 1.10.33 del "de Finibus Bonorum et Malorum" di Cicerone. Questo testo è un trattato su teorie di etica, molto popolare nel Rinascimento. La prima riga del Lorem Ipsum, "Lorem ipsum dolor sit amet..", è tratta da un passaggio della sezione 1.10.32.\n\nIl brano standard del Lorem Ipsum usato sin dal sedicesimo secolo è riprodotto qui di seguito per coloro che fossero interessati. Anche le sezioni 1.10.32 e 1.10.33 del "de Finibus Bonorum et Malorum" di Cicerone sono riprodotte nella loro forma originale, accompagnate dalla traduzione inglese del 1914 di H. Rackham.',
                  'lang_name': 'Italian',
                  'name': 'Giovanni',
                  'title': 'questa è una prova'},
                 {'comm_content': 'Mijn mening.',
                  'content': 'Da dove viene?\nAl contrario di quanto si pensi, Lorem Ipsum non è semplicemente una sequenza casuale di caratteri. Risale ad un classico della letteratura latina del 45 AC, cosa che lo rende vecchio di 2000 anni. Richard McClintock, professore di latino al Hampden-Sydney College in Virginia, ha ricercato una delle più oscure parole latine, consectetur, da un passaggio del Lorem Ipsum e ha scoperto tra i vari testi in cui è citata, la fonte da cui è tratto il testo, le sezioni 1.10.32 and 1.10.33 del "de Finibus Bonorum et Malorum" di Cicerone. Questo testo è un trattato su teorie di etica, molto popolare nel Rinascimento. La prima riga del Lorem Ipsum, "Lorem ipsum dolor sit amet..", è tratta da un passaggio della sezione 1.10.32.\n\nIl brano standard del Lorem Ipsum usato sin dal sedicesimo secolo è riprodotto qui di seguito per coloro che fossero interessati. Anche le sezioni 1.10.32 e 1.10.33 del "de Finibus Bonorum et Malorum" di Cicerone sono riprodotte nella loro forma originale, accompagnate dalla traduzione inglese del 1914 di H. Rackham.',
                  'lang_name': 'Dutch',
                  'name': 'Johan',
                  'title': 'Dit is een test'},
                 {'comm_content': 'Mielestäni.',
                  'content': 'Mistä se tulee?\nVastoin yleistä uskomusta, Lorem Ipsum ei ole vain sattumanvarainen teksti. Sillä on pitkät juuret klassisesta latinalaisesta kirjallisuudesta vuonna 45 eKr alkaen, tehden siitä yli 2000 vuotta vanhan. Richard McClintock, latinalainen professori Hampden-Sydneyn yliopistossa Virginiassa, etsi yhden vaikeaselkoisimmista latinalaisista sanoista, consectetur, Lorem Ipsumin kappaleesta ja etsi lainauksia sanasta klassisessa kirjallisuudessa löytäen varman lähteen. Lorem Ipsum tulee osista 1.10.32 ja 1.10.33 "de Finibus Bonorum et Malorum":ksesta (The Extremes of Good and Evil), jonka teki Cicero vuonna 45 eKr. Tämä kirja on tutkielma etiikasta, joka oli hyvin yleistä Renesanssin aikana. Ensimmäinen Lorem Ipsumin rivi, "Lorem ipsum dolor sit amet..", tulee rivistä joka on osassa 1.10.32.\n\nNormaali palanen Lorem Ipsumia, jota on käytetty 1500-luvulla on toistettu alla niille jotka ovat vain kiinnostuneita. Osiot 1.10.32 ja 1.10.33 "de Finibus Bonorum et Malorum":ksesta, Cicerolta, ovat myös toistettu niiden tarkoissa alkuperäisissä muodoissaan, joita seuraa englantilaiset versiot vuodelta 1914, kääntäjänä H. Rackman.',
                  'lang_name': 'Finnish',
                  'name': 'Jani',
                  'title': 'Tämä on testi'},
                 {'comm_content': 'Véleményem.',
                  'content': 'Honnan származik?\nA hiedelemmel ellentétben a Lorem Ipsum nem véletlenszerû szöveg. Gyökerei egy Kr. E. 45-ös latin irodalmi klasszikushoz nyúlnak. Richarrd McClintock a virginiai Hampden-Sydney egyetem professzora kikereste az ismeretlenebb latin szavak közül az egyiket (consectetur) egy Lorem Ipsum részletbõl, és a klasszikus irodalmat átkutatva vitathatatlan forrást talált. A Lorem Ipsum az 1.10.32 és 1.10.33-as de Finibus Bonoruem et Malorum részleteibõl származik (A Jó és Rossz határai - Cicero), Kr. E. 45-bõl. A könyv az etika elméletét tanulmányozza, ami nagyon népszerû volt a reneszánsz korban. A Lorem Ipsum elsõ sora, Lorem ipsum dolor sit amet.. a 1.10.32-es bekezdésbõl származik.\n\nA Lorem Ipsum alaprészlete, amit az 1500-as évek óta használtak, az érdeklõdõk kedvéért lent újra megtekinthetõ. Az 1.10.32 és 1.10.33-as bekezdéseket szintén eredeti formájukban reprodukálták a hozzá tartozó angol változattal az 1914-es fordításból H. Rackhamtól.',
                  'lang_name': 'Hungarian',
                  'name': 'Janos',
                  'title': 'Ez egy teszt'}]

def load_dummy_data():
    """
    Populates the database with placeholder content for functional tests purposes.

    """

    db.create_all()

    admin_role = Role.query.filter(Role.name == 'Admin').first_or_404()
    contributor_role = Role.query.filter(Role.name == 'Contributor').first_or_404()
    userone = User(username="admin_testing", displayname="admin_testing", email="admin_testing@example.com",
                   password="admin", roles=[admin_role],
                   confirmed=True, confirmed_on=datetime.datetime.utcnow())
    usertwo = User(username="user_testing", displayname="user_testing", email="user_testing@example.com",
                   password="user", roles=[contributor_role], confirmed=True, confirmed_on=datetime.datetime.utcnow())

    db.session.add(userone)
    db.session.add(usertwo)

    db.session.commit()

    for x, i in enumerate(DUMMY_CONTENT):
        tag = Tag(name=i['lang_name'])
        db.session.add(tag)

        post = Post(content=i['content'] * 3, title=i['title'], user=usertwo, tags=[tag], publish=True)
        db.session.add(post)

        comment = Comment(comment_user=userone, content=i['comm_content'], post_id=x + 1)
        db.session.add(comment)

    db.session.commit()

    print('Populated the database with test data.')

from datetime import datetime, timedelta
import random
from sqlalchemy import func
from passlib.hash import pbkdf2_sha256
from models import session, Recipe, User

# Returns random date in interval now to days back
def random_date(days_back=365):
    return (datetime.now() - timedelta(days=random.randint(1, days_back), hours=random.randint(0, 23), minutes=random.randint(0, 59))).isoformat()
# Returns random user
def random_user():
    user_count = session.query(func.count(User.id)).scalar()

    # Generate a random offset
    random_offset = random.randint(0, user_count - 1)

    # Query the user with the random offset
    return session.query(User).offset(random_offset).first()

def seed_users():
    users = [
        {
            "name": "test_user",
            "email": "test@test.cz",
            "password": pbkdf2_sha256.encrypt("123456789")
        },
        {
            "name": "Alice Nováková",
            "email": "alice@example.com",
            "password": pbkdf2_sha256.encrypt("securepassword1")
        },
        {
            "name": "Bob Novák",
            "email": "bob@example.com",
            "password": pbkdf2_sha256.encrypt("strongpassword2")
        },
        {
            "name": "Charlie Dvořák",
            "email": "charlie@example.com",
            "password": pbkdf2_sha256.encrypt("safepassword3")
        },
        {
            "name": "David Svoboda",
            "email": "david@example.com",
            "password": pbkdf2_sha256.encrypt("password4")
        },
        {
            "name": "Eva Černá",
            "email": "eva@example.com",
            "password": pbkdf2_sha256.encrypt("secretword5")
        },
    ]

    for user_data in users:
        user = User(**user_data)
        session.add(user)

    session.commit()


def seed_recipes():
    recipes = [
        {
            "name": "Špagety Boloňská omáčka",
            "date": random_date(),
            "author": random_user(),
            "ingredients": "200g špagety, 300g mleté hovězí maso, 1 cibule, 2 stroužky česneku, 400g konzervovaných rajčat, 1 lžička oregána, sůl, pepř",
            "description": "1. Uvařte špagety podle pokynů na obalu. \n2. Na pánvi osmažte mleté hovězí maso s nakrájenou cibulí a česnekem. \n3. Přidejte konzervovaná rajčata a okořeňte oregánem, solí a pepřem. \n4. Vařte, dokud omáčka nezhoustne. \n5. Podávejte omáčku ke uvařeným špagetám."
        },
        {
            "name": "Kuřecí Alfredo",
            "date": random_date(),
            "author": random_user(),
            "ingredients": "250g fettuccine, 2 kuřecí prsa, 1 šálek smetany ke šlehání, 1 šálek parmazánu, sůl, pepř, petržel",
            "description": "1. Uvařte fettuccine podle pokynů na obalu. \n2. Ochutnejte kuřecí prsa solí a pepřem, poté uvařte do hotova. \n3. V jiné pánvi ohřejte smetanu a přidejte parmazán. \n4. Nařežte uvařené kuřecí maso a smíchejte s omáčkou Alfredo. \n5. Podávejte přes uvařené fettuccine, ozdobte petrželí."
        },
        {
            "name": "Rajská polévka",
            "date": random_date(),
            "author": random_user(),
            "ingredients": "500g rajčat, 1 cibule, 2 brambory, 2 mrkve, 1 paprika, 1 lžíce oleje, sůl, pepř, tymián",
            "description": "1. Nakrájejte rajčata, cibuli, brambory, mrkev a papriku na kousky. \n2. Na pánvi rozehřejte olej a osmažte cibuli. \n3. Přidejte rajčata, brambory, mrkev a papriku. Podlijte vodou. \n4. Vařte do měkka. Přidávejte sůl, pepř a tymián podle chuti. \n5. Podávejte teplou."
        },
        {
            "name": "Bramborový Guláš",
            "date": random_date(),
            "author": random_user(),
            "ingredients": "1kg brambor, 2 cibule, 3 lžíce oleje, 2 lžíce sladké papriky, 400g nakrájeného masa (hovězí nebo vepřové), sůl, pepř, kmín",
            "description": "1. Nakrájejte brambory a cibuli na kostky. \n2. Na pánvi rozehřejte olej a osmažte cibuli. Přidejte sladkou papriku. \n3. Přidejte nakrájené maso a osmažte dozlatova. \n4. Přidejte brambory, sůl, pepř a kmín. \n5. Vařte do měkka. Podávejte teplý guláš."
        },
        {
            "name": "Ryba na zeleninové posteli",
            "date": random_date(),
            "author": random_user(),
            "ingredients": "500g rybího filetu, 1 cuketa, 1 lilek, 2 rajčata, olivový olej, česnek, sůl, citron, petržel",
            "description": "1. Na plech nasypte na plátek olivového oleje. Položte na něj rybí filet. \n2. Na filet posypte nasekaný česnek, sůl a zakápějte citronovou šťávou. \n3. Zeleninu nakrájejte na plátky a položte kolem ryby. \n4. Pečte v troubě dozlatova. \n5. Podávejte posypané nasekanou petrželí."
        },
        {
            "name": "Česnečka s vejcem",
            "date": random_date(),
            "author": random_user(),
            "ingredients": "4 stroužky česneku, 1 cibule, 1 lžíce oleje, 1 lžíce hladké mouky, 1 lžíce octa, 1 lžička cukru, 1 vejce, sůl, kmín",
            "description": "1. Na pánvi osmažte nasekaný česnek a cibuli na oleji. \n2. Přidejte hladkou mouku a smažte dozlatova. \n3. Přidejte ocet, cukr, sůl a kmín. Podlijte vodou a vařte 10 minut. \n4. Do polévky přidejte uvařené vejce nakrájené na kolečka. \n5. Podávejte teplou česnečku."
        },
        {
            "name": "Vepřová pečeně se švestkami",
            "date": random_date(),
            "author": random_user(),
            "ingredients": "1kg vepřové pečeně, 200g švestek, 2 cibule, 2 lžíce medu, 1 lžíce hořčice, tymián, sůl, pepř",
            "description": "1. Vepřovou pečeni osolte, opepřete a natřete medem smíchaným s hořčicí. \n2. Nakrájejte cibule na plátky a švestky na čtvrtky. \n3. Vše položte kolem pečeně, posypte tymiánem. \n4. Pečte v troubě dozlatova. \n5. Podávejte se zeleninovou přílohou."
        },
        {
            "name": "Hovězí guláš s knedlíkem",
            "date": random_date(),
            "author": random_user(),
            "ingredients": "500g hovězího masa, 2 cibule, 3 lžíce oleje, 2 lžíce sladké papriky, sůl, pepř, kmín, 1 balíček knedlíkové směsi",
            "description": "1. Maso nakrájejte na kostky a osolte. \n2. Na pánvi rozehřejte olej a osmažte cibuli. Přidejte sladkou papriku. \n3. Přidejte nakrájené maso a osmažte dozlatova. \n4. Přidejte sůl, pepř, kmín a podlijte vodou. Vařte do měkka. \n5. Připravte knedlíky podle návodu na obalu."
        },
        {
            "name": "Kuřecí salát s jogurtem",
            "date": random_date(),
            "author": random_user(),
            "ingredients": "300g kuřecího masa, 1 hlávkový salát, 2 rajčata, 1 okurka, 1 paprika, 1 jogurt, 1 lžíce hořčice, sůl, pepř",
            "description": "1. Kuřecí maso uvařte a nakrájejte na kousky. \n2. Nakrájejte salát, rajčata, okurku a papriku na menší kousky. \n3. V míse smíchejte jogurt s hořčicí, solí a pepřem. \n4. Přidejte nakrájené ingredience a kuřecí maso. \n5. Dobře promíchejte a podávejte chladné."
        },
        {
            "name": "Těstovinový salát s tuňákem",
            "date": random_date(),
            "author": random_user(),
            "ingredients": "300g těstovin, 1 plechovka tuňáka, 1 červená cibule, 1 paprika, 1 okurka, majonéza, sůl, pepř, koriandr",
            "description": "1. Těstoviny uvařte podle pokynů na obalu. \n2. Nakrájejte cibuli, papriku a okurku na drobné kousky. \n3. V míse smíchejte uvařené těstoviny, tuňáka, nakrájenou zeleninu, majonézu, sůl, pepř a koriandr. \n4. Dobře promíchejte a podávejte chladné."
        },
        {
            "name": "Ovocný koláč s tvarohem",
            "date": random_date(),
            "author": random_user(),
            "ingredients": "250g tvarohu, 3 vejce, 200g cukru, 200g mouky, 1 prášek do pečiva, 1 vanilkový cukr, ovoce podle chuti",
            "description": "1. Tvaroh smíchejte s vejci, cukrem, moukou, práškem do pečiva a vanilkovým cukrem. \n2. Těsto nalijte do formy a rozetřete ho. \n3. Na těsto položte ovoce podle chuti. \n4. Pečte v troubě dozlatova. \n5. Podávejte po vychladnutí."
        },
        {"name": "Svíčková na smetaně",
            "date": random_date(),
            "author": random_user(),
            "ingredients": "800g hovězí svíčková, 2 cibule, 2 mrkve, 1 petržel, 3 lžíce oleje, 1 lžíce hladké mouky, 2 lžíce rajského protlaku, 1 lžíce hořčice, 300ml smetany, sůl, pepř, bobkový list",
            "description": "1. Ochucenou svíčkovou osolte, opepřete a obložte nakrájenými zeleninovými kousky. \n2. Na rozpáleném oleji osmažte z obou stran. \n3. Přidejte hladkou mouku, orestujte a zalijte vodou. \n4. Přidejte rajský protlak, hořčici a bobkový list. \n5. Vařte, dokud maso není měkké. \n6. Přidejte smetanu, promíchejte a podávejte s houskovým knedlíkem."
        },
        {
            "name": "Knedlíky se švestkovou omáčkou",
            "date": random_date(),
            "author": random_user(),
            "ingredients": "300g bramborového těsta na knedlíky, 300g švestek, 3 lžíce cukru, 1 lžíce másla, skořice",
            "description": "1. Uvařte bramborové těsto na knedlíky podle návodu. \n2. Švestky omyjte, očistěte a nakrájejte na kousky. \n3. V hrnci smíchejte švestky, cukr, máslo a skořici. \n4. Povařte do měkka švestek a vytvoření omáčky. \n5. Knedlíky uvařte a podávejte zalité švestkovou omáčkou."
        },
        {
            "name": "Česká Bramborová Polévka",
            "date": random_date(),
            "author": random_user(),
            "ingredients": "4 velké brambory, 2 cibule, 2 stroužky česneku, 1 lžíce oleje, 1 lžíce hladké mouky, 1 litr zeleninového vývaru, 1/2 lžičky majoránky, sůl, pepř",
            "description": "1. Brambory oloupejte a nakrájejte na kostičky. \n2. Na oleji osmažte cibuli a česnek. \n3. Přidejte brambory a nechte chvilku restovat. \n4. Přidejte hladkou mouku a za stálého míchání zalijte zeleninovým vývarem. \n5. Přidejte majoránku, osolte a opepřete. \n6. Vařte do měkka brambor. Podávejte s kousky chleba."
        },
        {
            "name": "Vepřo-knedlo-zelo",
            "date": random_date(),
            "author": random_user(),
            "ingredients": "500g vepřového masa, 1 cibule, 1 lžíce sádla, 1 hlávka zelí, 1 lžíce kmínu, 1 lžíce majoránky, sůl, pepř, houskové knedlíky",
            "description": "1. Maso nakrájejte na kostky a osmažte na sádle s cibulí. \n2. Přidejte na nudle nakrájené zelí a poduste. \n3. Přidejte kmín, majoránku, sůl a pepř podle chuti. \n4. Duste pod pokličkou do měkka masa. \n5. Podávejte s houskovými knedlíky."
        },
        {
            "name": "Koláč s ovocem",
            "date": random_date(),
            "author": random_user(),
            "ingredients": "200g hladké mouky, 100g másla, 1/2 lžičky soli, 1 lžíce cukru, 2 lžíce studené vody, ovoce dle chuti (třešně, meruňky, jahody), cukr na posypání",
            "description": "1. Smíchejte mouku, sůl a cukr. \n2. Přidejte na kostky nakrájené máslo a hněte těsto. \n3. Přidejte studenou vodu a vytvořte hladké těsto. \n4. Těsto rozválejte a umístěte do formy. \n5. Ovoce rovnoměrně rozložte na těsto. \n6. Posypte cukrem a upečte dozlatova."
        },
        {
            "name": "Česnečka",
            "date": random_date(),
            "author": random_user(),
            "ingredients": "4 brambory, 3 stroužky česneku, 1 lžíce oleje, 1 lžíce hladké mouky, 1 lžíce octa, 2 vejce, sůl, majoránka, chleba",
            "description": "1. Brambory oloupejte, nakrájejte na kostičky a uvařte. \n2. Na oleji osmažte na nudle nakrájený česnek. \n3. Přidejte hladkou mouku, promíchejte. \n4. Přidejte ocet, osolte a podlijte vodou. \n5. Přiveďte k varu a přidejte uvařené brambory. \n6. Podávejte s vejcem, posypané majoránkou a chlebem."
        },
        {
            "name": "Trdelník",
            "date": random_date(),
            "author": random_user(),
            "ingredients": "500g hladké mouky, 250ml mléka, 75g másla, 1 žloutek, 1 lžička soli, 10g droždí, 100g moučkového cukru, 1 lžíce skořice",
            "description": "1. V hrnci ohřejte mléko a rozpusťte v něm máslo. \n2. Do misky nasypejte mouku, přidejte žloutek, rozdrobte droždí a přidejte sůl. \n3. Přilijte mléko s máslem a vytvořte těsto. \n4. Těsto nechte kynout. \n5. Z těsta tvarujte válečky, obalte v cukru a skořici. \n6. Pečte v troubě nebo na otáčivém grilu. \n7. Podávejte posypané moučkovým cukrem."
        },
        {
            "name": "Špenátový Karbanátek",
            "date": random_date(),
            "author": random_user(),
            "ingredients": "500g mletého masa (hovězí nebo vepřové), 200g čerstvého špenátu, 1 cibule, 2 stroužky česneku, 1 vejce, 3 lžíce strouhanky, sůl, pepř, olej na smažení",
            "description": "1. Špenát nastrouhejte, cibuli a česnek nasekejte. \n2. Smíchejte mleté maso se špenátem, cibulí, česnekem, vejcem a strouhankou. \n3. Ochutnejte solí a pepřem. \n4. Tvarujte karbanátky a smažte na rozpáleném oleji dozlatova. \n5. Podávejte s bramborovým salátem."
        },
        {
            "name": "Rajská omáčka s klobásou",
            "date": random_date(),
            "author": random_user(),
            "ingredients": "500g rajčat, 1 cibule, 2 stroužky česneku, 300g klobásy, 1 lžíce oleje, sůl, pepř, bazalka, 300g těstovin",
            "description": "1. Rajčata oloupejte a nakrájejte. \n2. Na oleji osmažte nakrájenou cibuli a česnek. \n3. Přidejte rajčata a vařte do zhoustnutí. \n4. Přidejte nakrájenou klobásu a vařte do měkka. \n5. Ochutnejte solí, pepřem a bazalkou. \n6. Podávejte s uvařenými těstovinami."
        },{
            "name": "Kuřecí Paprikáš",
            "date": random_date(),
            "author": random_user(),
            "ingredients": "500g kuřecího masa, 2 cibule, 2 papriky, 2 lžíce oleje, 2 lžíce mleté papriky, 200ml smetany, sůl, pepř, kmín",
            "description": "1. Kuřecí maso nakrájejte na kousky. \n2. Na oleji osmažte cibuli a papriky. \n3. Přidejte kuřecí maso a mletou papriku. \n4. Podlijte vodou a vařte do měkka. \n5. Přidejte smetanu, osolte, opepřete a přidejte kmín. \n6. Podávejte s knedlíky nebo rýží."
        },
        {
            "name": "Buchty se švestkovou nádivkou",
            "date": random_date(),
            "author": random_user(),
            "ingredients": "500g hladké mouky, 200ml mléka, 75g másla, 2 žloutky, 1 vanilkový cukr, 1 balíček suchého droždí, švestky, moučkový cukr",
            "description": "1. V hrnci ohřejte mléko a rozpusťte v něm máslo. \n2. Do mísy nasypejte mouku, přidejte žloutky, vanilkový cukr, a rozdrobené droždí. \n3. Přilijte mléko s máslem a vytvořte těsto. \n4. Těsto nechte kynout. \n5. Očištěné švestky rozkrojte a odstraňte pecky. \n6. Těsto rozválejte, nakrájejte na čtverce a na každý položte švestku. \n7. Buchty srolujte, položte na plech a nechte ještě chvilku kynout. \n8. Pečte v troubě. \n9. Podávejte posypané moučkovým cukrem."
        },
        {
            "name": "Zelňačka",
            "date": random_date(),
            "author": random_user(),
            "ingredients": "1 hlávka zelí, 2 cibule, 2 brambory, 1 lžíce oleje, 1 lžíce hladké mouky, 2 lžíce octa, 1 lžíce cukru, sůl, pepř, kmín, majoránka",
            "description": "1. Zelí nasekejte na jemno, cibuli nakrájejte, brambory oloupejte a nakrájejte na kostičky. \n2. Na oleji osmažte cibuli a přidejte zelí. \n3. Přidejte brambory a zalijte vodou. \n4. Přiveďte k varu a vařte do měkka. \n5. Přidejte hladkou mouku, ocet, cukr, sůl, pepř, kmín a majoránku. \n6. Vařte ještě chvilku. \n7. Podávejte s klobásou nebo nakládaným masem."
        },
        {
            "name": "Halušky s brynzou a slaninou",
            "date": random_date(),
            "author": random_user(),
            "ingredients": "500g brambor, 300g hladké mouky, 200g bryndza, 150g slaniny, sůl, olej",
            "description": "1. Brambory oloupejte, nastrouhejte a smíchejte s moukou. \n2. Těsto rozdělte na menší části a vytvarujte válečky. \n3. Vařte v osolené vodě. \n4. Bryndzu rozetřete. \n5. Na pánvi osmažte na kostičky nakrájenou slaninu. \n6. Uvařené halušky smíchejte s brynzou a osmaženou slaninou. \n7. Podávejte posypané smaženou cibulkou."
        },
        {
            "name": "Sýrové šišky",
            "date": random_date(),
            "author": random_user(),
            "ingredients": "500g brambor, 100g strouhanku, 2 vejce, 150g niva sýra, sůl, olej",
            "description": "1. Brambory oloupejte, nastrouhejte a vymačkejte nadbytečnou vodu. \n2. Přidejte strouhanku, vejce, nastrouhaný sýr a sůl. \n3. Dobře promíchejte a vytvářejte malé kuličky. \n4. Smažte na rozpáleném oleji dozlatova. \n5. Podávejte s tatarskou omáčkou nebo kečupem."
        },
        {
            "name": "Pražská Šunka v Medu",
            "date": random_date(),
            "author": random_user(),
            "ingredients": "500g pražské šunky, 3 lžíce medu, 2 lžíce hořčice, 1 lžička kmínu",
            "description": "1. Pražskou šunku nařežte. \n2. Smíchejte med, hořčici a kmín. \n3. Namasírujte směsí každý kousek šunky. \n4. Dejte do trouby a pečte dozlatova. \n5. Podávejte se zelím nebo bramborovým salátem."
        },
        {
            "name": "Tvarohová Bábovka",
            "date": random_date(),
            "author": random_user(),
            "ingredients": "250g tvarohu, 3 vejce, 200g cukru, 250g hladké mouky, 1 lžička prášku do pečiva, 100ml oleje, citronová kůra",
            "description": "1. Tvaroh smíchejte s cukrem a žloutky. \n2. Přidejte mouku s práškem do pečiva, olej a citronovou kůru. \n3. Vymíchejte. \n4. Bílky ušlehejte a opatrně vmíchejte do těsta. \n5. Pečte v troubě dozlatova. \n6. Podávejte posypané cukrem."
        },
        {
            "name": "Česnekový Smažený Hermelín",
            "date": random_date(),
            "author": random_user(),
            "ingredients": "1 kus Hermelín, 2 stroužky česneku, 2 lžíce oleje, sůl, tymián, křen, chleba",
            "description": "1. Hermelín nakrájejte na plátky. \n2. Na pánvi na oleji osmažte nakrájený česnek. \n3. Přidejte plátky Hermelínu a smažte dozlatova. \n4. Ochutnejte solí a tymiánem. \n5. Podávejte s křenem a čerstvým chlebem."
        },
        {
            "name": "Český Goulash",
            "date": random_date(),
            "author": random_user(),
            "ingredients": "600g hovězího masa, 2 cibule, 2 papriky, 2 lžíce oleje, 2 lžíce mleté papriky, 1 lžíce hladké mouky, 500ml hovězího vývaru, sůl, pepř, kmín",
            "description": "1. Hovězí maso nakrájejte na kostky. \n2. Na oleji osmažte cibuli a papriky. \n3. Přidejte hovězí maso a mletou papriku. \n4. Duste pod víkem do změknutí masa. \n5. Přidejte hladkou mouku, zalijte vývarem a vařte dohromady. \n6. Ochutnejte solí, pepřem a kmínem. \n7. Podávejte s knedlíky nebo chlebem."
        },
        {
            "name": "Švestkový Knedlík",
            "date": random_date(),
            "author": random_user(),
            "ingredients": "500g brambor, 150g hrubé mouky, 1 vejce, špetka soli, švestky, mák, moučkový cukr",
            "description": "1. Brambory uvařte, oloupejte a nastrouhejte. \n2. Přidejte mouku, vejce a špetku soli. \n3. Vytvořte těsto a rozdělte ho na menší kousky. \n4. Do každého kousku dejte švestku a vytvořte knedlík. \n5. Uvařte ve vařící vodě. \n6. Podávejte posypané mákem a moučkovým cukrem."
        },
    ]

    for recipe_data in recipes:
        recipe = Recipe(**recipe_data)
        session.add(recipe)

    session.commit()



seed_users()
seed_recipes()
print("Database seeded!")
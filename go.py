import requests
import pandas as pd
import time

# Function to fetch GO annotations for a single UniProt ID
def get_go_annotations(uniprot_id):
    url = f"https://www.uniprot.org/uniprot/{uniprot_id}.txt"
    response = requests.get(url)
    if response.status_code == 200:
        go_terms = []
        for line in response.text.splitlines():
            if line.startswith("DR   GO;"):
                go_term = line.split(";")[1].strip()
                go_terms.append(go_term)
        return go_terms
    else:
        print(f"Failed to fetch data for {uniprot_id}")
        return []

# Input data as a dictionary (simulating the provided data)
data = [
    {"id": "A0A286YD05", "ec": "1.14.11.68", "interpro": "IPR051630;IPR003347;IPR046941;IPR048562;IPR048560;"},
    {"id": "F2Z438", "ec": "2.1.1.85", "interpro": "IPR046341;IPR025785;"},
    {"id": "D3Z4X1", "ec": "3.1.1.31", "interpro": "IPR005900;IPR006148;IPR037171;IPR039104;"},
    {"id": "A0A1L1SV73", "ec": "3.4.19.12", "interpro": "IPR038765;IPR050164;IPR001394;IPR029071;IPR045578;IPR018200;IPR028889;"},
    {"id": "E9QL53", "ec": "2.7.11.1", "interpro": "IPR000961;IPR046349;IPR017405;IPR001180;IPR037708;IPR011009;IPR002219;IPR011993;IPR001849;IPR017892;IPR000719;IPR017441;IPR050839;IPR008271;"},
    {"id": "Q3V1N7", "ec": "1.2.1.19", "interpro": "IPR016161;IPR016163;IPR016160;IPR029510;IPR016162;IPR015590;"},
    {"id": "Q7TS65", "ec": "2.7.11.24", "interpro": "IPR011009;IPR050117;IPR000719;"},
    {"id": "Q5J7N1", "ec": "3.6.5.2", "interpro": "IPR027417;IPR005225;IPR001806;IPR020849;"},
    {"id": "Q99N99", "ec": "1.3.1.22", "interpro": "IPR016636;IPR001104;IPR039357;"},
    {"id": "Q3U258", "ec": "2.7.11.1", "interpro": "IPR011009;IPR051511;IPR040110;IPR000719;IPR017441;IPR008271;"},
    {"id": "P27808", "ec": "2.4.1.101", "interpro": "IPR004139;IPR052261;IPR029044;"},
    {"id": "Q7TPX2", "ec": "3.1.1.4", "interpro": "IPR016035;IPR002110;IPR036770;IPR047148;IPR002641;"},
    {"id": "A0A338P6T6", "ec": "3.6.1.52", "interpro": "IPR047198;IPR015797;IPR020084;IPR000086;"},
    {"id": "B2RX12", "ec": "7.6.2.-", "interpro": "IPR003593;IPR011527;IPR036640;IPR003439;IPR017871;IPR050173;IPR005292;IPR027417;"},
    {"id": "Q3TV21", "ec": "1.16.3.1", "interpro": "IPR017789;IPR002908;IPR036524;IPR020895;"},
    {"id": "Q7TPZ8", "ec": "3.4.17.1", "interpro": "IPR034248;IPR036990;IPR003146;IPR000834;"},
    {"id": "Q3UYS0", "ec": "6.4.1.3", "interpro": "IPR051047;IPR034733;IPR029045;IPR011763;IPR011762;"},
    {"id": "A0A0R4J083", "ec": "1.3.8.8", "interpro": "IPR006089;IPR006091;IPR046373;IPR036250;IPR009075;IPR013786;IPR037069;IPR009100;IPR034179;"},
    {"id": "P51569", "ec": "3.2.1.22", "interpro": "IPR013785;IPR002241;IPR000111;IPR013780;IPR017853;IPR035373;"},
    {"id": "Q9QZR5", "ec": "2.7.11.1", "interpro": "IPR011009;IPR000719;IPR017441;IPR008271;IPR050494;"},
    {"id": "Q6WIZ9", "ec": "2.3.2.31", "interpro": "IPR047543;IPR047540;IPR002867;IPR036339;IPR018997;IPR047542;IPR026254;IPR032065;IPR041031;IPR040641;IPR047541;IPR044066;IPR015940;IPR047539;IPR001876;IPR036443;IPR013083;IPR017907;"},
    {"id": "P70269", "ec": "3.4.23.34", "interpro": "IPR001461;IPR001969;IPR012848;IPR033121;IPR021109;"},
    {"id": "Q8BUB9", "ec": "3.6.4.12", "interpro": "IPR051493;IPR016197;IPR000953;IPR023780;IPR014001;IPR027417;IPR038718;IPR000330;"},
    {"id": "Q8C1A8", "ec": "6.2.1.1", "interpro": "IPR032387;IPR025110;IPR045851;IPR020845;IPR000873;IPR042099;"},
    {"id": "Q05DM4", "ec": "4.2.1.1", "interpro": "IPR001148;IPR036398;IPR023561;"},
    {"id": "Q4V9V3", "ec": "2.3.1.199", "interpro": "IPR030457;IPR002076;"},
    {"id": "Q8R0N6", "ec": "1.1.99.24", "interpro": "IPR001670;IPR039697;IPR042157;"},
    {"id": "Q3UNR3", "ec": "6.2.1.3", "interpro": "IPR025110;IPR045851;IPR020845;IPR000873;IPR042099;"},
    {"id": "Q60669", "ec": "2.7.10.1", "interpro": "IPR027936;IPR001090;IPR050449;IPR003961;IPR036116;IPR008979;IPR009030;IPR013783;IPR011009;IPR000719;IPR017441;IPR001660;IPR013761;IPR001245;IPR011641;IPR008266;IPR020635;IPR016257;IPR001426;"},
    {"id": "Q9CRA4", "ec": "1.14.18.9", "interpro": "IPR006694;IPR050307;"},
    {"id": "Q3UC49", "ec": "4.98.1.1", "interpro": "IPR001015;IPR019772;IPR033644;IPR033659;"},
    {"id": "A0A0R4J0R4", "ec": "2.3.1.17", "interpro": "IPR016181;IPR050769;IPR000182;"},
    {"id": "Q8CFX1", "ec": "1.1.1.47", "interpro": "IPR005900;IPR001282;IPR019796;IPR022675;IPR022674;IPR006148;IPR036291;IPR037171;"},
    {"id": "E9Q7E8", "ec": "2.7.10.1", "interpro": "IPR016248;IPR007110;IPR036179;IPR013783;IPR013098;IPR003599;IPR003598;IPR011009;IPR000719;IPR017441;IPR050122;IPR001245;IPR008266;IPR020635;"},
    {"id": "A0A286YCZ0", "ec": "1.2.1.19", "interpro": "IPR016161;IPR016162;IPR015590;"},
    {"id": "D3Z2K9", "ec": "3.6.4.12", "interpro": "IPR031327;IPR008050;IPR033762;IPR012340;"},
    {"id": "F6RP11", "ec": "2.7.4.6", "interpro": "IPR000850;IPR007862;IPR036193;IPR027417;"},
    {"id": "Q8BP74", "ec": "2.7.1.164", "interpro": "IPR013641;IPR020028;IPR027417;IPR052648;"},
    {"id": "E9Q364", "ec": "2.7.11.1", "interpro": "IPR011009;IPR000719;IPR017441;IPR051234;"},
    {"id": "Q9D2H2", "ec": "2.7.4.3", "interpro": "IPR000850;IPR047499;IPR007858;IPR036291;IPR027417;"},
    {"id": "Q8R2M8", "ec": "2.1.1.216", "interpro": "IPR029063;IPR002905;IPR042296;IPR000571;IPR036855;"},
    {"id": "D3Z423", "ec": "2.3.2.27", "interpro": "IPR042123;IPR017907;"},
    {"id": "C0HKC9", "ec": "2.7.11.1", "interpro": "IPR011009;IPR000719;IPR008271;"},
    {"id": "Q8BMZ5", "ec": "4.6.1.16", "interpro": "IPR011856;IPR036167;IPR006677;IPR006676;IPR016690;"},
    {"id": "Q5DTF9", "ec": "2.4.1.135", "interpro": "IPR005027;IPR029044;"},
    {"id": "Q8BH86", "ec": "4.2.1.48", "interpro": "IPR009906;IPR017135;IPR025504;IPR038021;"},
    {"id": "Q9D9D8", "ec": "3.1.3.16", "interpro": "IPR020420;IPR000340;IPR029021;IPR016130;IPR000387;IPR020422;"},
    {"id": "G3UZN8", "ec": "1.14.11.80", "interpro": "IPR024779;IPR040175;"},
    {"id": "Q3TNX8", "ec": "3.4.24.82", "interpro": "IPR006586;IPR013273;IPR050439;IPR041645;IPR045371;IPR010294;IPR024079;IPR001590;IPR000884;IPR036383;"},
    {"id": "B3DFI9", "ec": "2.3.2.27", "interpro": "IPR044046;IPR039164;"},
    {"id": "Q9DCS3", "ec": "1.3.1.104", "interpro": "IPR013149;IPR013154;IPR011032;IPR051034;IPR036291;IPR020843;"},
    {"id": "P70288", "ec": "3.5.1.98", "interpro": "IPR050284;IPR000286;IPR003084;IPR023801;IPR037138;IPR023696;"},
    {"id": "B1ARD1", "ec": "2.1.1.71", "interpro": "IPR024960;IPR007318;"},
    {"id": "O54850", "ec": "2.7.7.49", "interpro": "IPR043502;IPR036691;IPR005135;IPR000477;"},
    {"id": "Q61846", "ec": "2.7.11.1", "interpro": "IPR028375;IPR001772;IPR011009;IPR034673;IPR048637;IPR000719;IPR017441;IPR008271;"},
    {"id": "G5E8I7", "ec": "3.4.19.12", "interpro": "IPR038765;IPR050164;IPR001394;IPR018200;IPR028889;"},
    {"id": "Q3UMW7", "ec": "2.7.11.1", "interpro": "IPR050205;IPR011009;IPR027442;IPR000719;IPR017441;IPR008271;"},
    {"id": "G3X9Q4", "ec": "6.1.1.20", "interpro": "IPR006195;IPR045864;IPR005121;IPR036690;IPR004530;IPR002319;"},
    {"id": "Q9CS42", "ec": "2.7.6.1", "interpro": "IPR000842;IPR029099;IPR000836;IPR029057;IPR005946;IPR037515;"},
    {"id": "Q3UKS0", "ec": "6.2.1.15", "interpro": "IPR020845;IPR000873;IPR042099;IPR045311;"},
    {"id": "B1AUY8", "ec": "2.3.1.255", "interpro": "IPR016181;IPR045047;IPR000182;"},
    {"id": "B2RU80", "ec": "3.1.3.48", "interpro": "IPR003961;IPR036116;IPR013783;IPR029021;IPR000242;IPR041201;IPR050713;IPR016130;IPR003595;IPR000387;"},
    {"id": "Q69ZY0", "ec": "5.1.3.17", "interpro": "IPR010598;IPR039721;"},
    {"id": "Q8R1G5", "ec": "6.3.3.2", "interpro": "IPR002698;IPR024185;IPR037171;"},
    {"id": "Q9JHT8", "ec": "3.1.3.11", "interpro": "IPR000146;IPR033391;"},
    {"id": "Q71UK2", "ec": "4.2.1.1", "interpro": "IPR001148;IPR036398;IPR023561;"},
    {"id": "Q6Q783", "ec": "2.1.1.362", "interpro": "IPR041938;IPR044425;IPR001214;IPR046341;IPR039977;IPR025790;"},
    {"id": "V9GZR3", "ec": "2.7.12.1", "interpro": "IPR051175;IPR011009;IPR000719;IPR017441;"},
    {"id": "Q3UDM3", "ec": "2.5.1.18", "interpro": "IPR023352;IPR001129;IPR040162;"},
    {"id": "A0AAG1F6P4", "ec": "3.4.19.12", "interpro": "IPR016024;IPR038765;IPR050164;IPR001394;IPR015940;IPR009060;IPR029071;IPR047061;IPR033382;IPR018200;IPR028889;"},
    {"id": "A0A1B0GT92", "ec": "2.4.1.11", "interpro": "IPR008631;"},
    {"id": "Q3UEG6", "ec": "2.6.1.44", "interpro": "IPR005814;IPR049704;IPR015424;IPR015421;IPR015422;"},
    {"id": "B2RWB7", "ec": "3.1.3.46", "interpro": "IPR013078;IPR029033;IPR001345;IPR051695;"},
    {"id": "A0A5F8MPN4", "ec": "1.14.13.225", "interpro": "IPR022735;IPR001715;IPR036872;IPR050540;IPR002938;IPR036188;IPR001781;"},
    {"id": "P56376", "ec": "3.6.1.7", "interpro": "IPR020456;IPR001792;IPR036046;IPR017968;"},
    {"id": "Q80UL3", "ec": "2.7.1.6", "interpro": "IPR000705;IPR019741;IPR019539;IPR013750;IPR036554;IPR006204;IPR006203;IPR006206;IPR020568;IPR014721;"},
    {"id": "Q3U1X4", "ec": "2.7.10.1", "interpro": "IPR030658;IPR007110;IPR036179;IPR013783;IPR003599;IPR003598;IPR013151;IPR011009;IPR000719;IPR017441;IPR050122;IPR001245;IPR008266;IPR020635;IPR001824;"},
    {"id": "Q61706", "ec": "2.7.7.49", "interpro": "IPR017856;IPR036862;IPR001037;IPR001584;IPR003308;IPR012337;IPR002156;IPR036397;"},
    {"id": "Q9D997", "ec": "2.7.1.59", "interpro": "IPR002731;IPR043129;IPR039758;"},
    {"id": "A0A0R4J260", "ec": "3.4.19.12", "interpro": "IPR003323;IPR050704;IPR038765;"},
    {"id": "A0A0A6YXY1", "ec": "2.1.1.244", "interpro": "IPR008576;IPR029063;"},
    {"id": "Q9D4E9", "ec": "3.2.1.35", "interpro": "IPR013785;IPR017853;IPR018155;"},
    {"id": "Q9CXX6", "ec": "2.6.1.42", "interpro": "IPR001544;IPR018300;IPR036038;IPR005786;IPR043132;IPR043131;IPR033939;"},
    {"id": "P58467", "ec": "2.1.1.-", "interpro": "IPR015353;IPR036464;IPR001214;IPR046341;IPR016852;IPR050600;IPR044429;"},
    {"id": "F6ZS70", "ec": "2.7.11.1", "interpro": "IPR028375;IPR001772;IPR011009;IPR049508;IPR000719;IPR017441;IPR008271;IPR015940;"},
    {"id": "E9Q7Q8", "ec": "2.4.2.31", "interpro": "IPR050999;IPR000768;"},
    {"id": "Q9DBV3", "ec": "3.6.4.13", "interpro": "IPR011709;IPR011545;IPR048333;IPR007502;IPR014001;IPR001650;IPR027417;"},
    {"id": "E9Q5B5", "ec": "2.7.1.1", "interpro": "IPR043129;IPR001312;IPR019807;IPR022673;IPR022672;"},
]

# Convert to a DataFrame for easier processing
df = pd.DataFrame(data)

# Add a column to store GO annotations
df["go_annotations"] = None

# Fetch GO terms for each ID and update the DataFrame
for index, row in df.iterrows():
    go_terms = get_go_annotations(row["id"])
    df.at[index, "go_annotations"] = go_terms
    time.sleep(1)  # To avoid overwhelming the UniProt server

# Save the results to a CSV file
df.to_csv("proteins_with_go_annotations.csv", index=False)

# Print the DataFrame
print(df)


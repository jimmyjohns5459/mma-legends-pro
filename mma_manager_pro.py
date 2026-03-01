import random, time, os, sys, re, pickle, pathlib

# ─── WEIGHT CLASSES ────────────────────────────────────────────────────────────
MEN_WEIGHT_CLASSES = [
    "Flyweight (125 lbs)", "Bantamweight (135 lbs)", "Featherweight (145 lbs)",
    "Lightweight (155 lbs)", "Welterweight (170 lbs)", "Middleweight (185 lbs)",
    "Light Heavyweight (205 lbs)", "Heavyweight (265 lbs)",
]

FIRST_NAMES = [
    # American
    "Jon","Jake","Mike","Tony","Nick","Nate","Donald","Tyron","Jorge","Colby",
    "Alex","Charles","Dustin","Justin","Sean","Max","Randy","Brock","Cain","Daniel",
    "Leon","Paulo","Kevin","Bobby","Eddie","Brian","Derek","Calvin","Deron",
    "Derrick","Khalil","Johnny","Chael","Forrest","Rashad","Quinton","Evan","Matt",
    "Curtis","Robbie","Anthony","Demetrious","Ryan","Brendan","Cody",
    "Henry","Alistair","Tim","Travis","Marvin","Thiago","Walt","Beneil",
    "Shane","Keith","Ricardo","Andre","Marcus","Ray","Shawn","Jerome","Tyson",
    # European / British / Irish
    "Conor","Paddy","Tom","Dan","Mark","Joe","Luke","Chris","David","Robert",
    "Stefan","Jan","Jiri","Gegard","Gunnar","Jack","Michael","Karl","James","Liam",
    "Owen","Harry","Finn","Darren","John","Paul","Simon","Brad","Craig",
    # Russian / Dagestani / Central Asian
    "Islam","Khamzat","Fedor","Petr","Arman","Umar","Said","Marat","Vitali","Artur",
    "Zabit","Magomed","Ruslan","Timur","Shamil","Movsar","Zubaira",
    "Aslan","Bekzod","Tagir","Mansur","Abubakar","Baurzhan","Sergei","Denis","Maxim",
    # Brazilian
    "Anderson","Jose","Fabricio","Vitor","Wanderlei","Lyoto","Glover","Edson",
    "Deiveson","Brandon","Rogerio","Gabriel","Wellington","Ronaldo","Junior","Rafael",
    "Renato","Gleison","Lucas","Felipe","Marcos","Hugo","Patrick","Warlley","Caio",
    # Pacific / African / Asian
    "Stipe","Francis","Ciryl","Tai","Israel","Ilia","George","Kamaru","Alexander",
    "Yair","Sodiq","Khalid","Nathaniel","Kyung-Ho","Seung-Woo",
    "Devin","Terrance","Vicente","Belal","Shavkat","Ikram","Manel",
    # Japanese / Korean
    "Takanori","Kazushi","Norifumi","Yoshihiro","Ryo","Tatsuya","Naoki","Seiya",
    "Tatsuro","Dong-Hyun","Chan-Sung","Doo-Ho","Jin-Soo",
    # Extra to pad roster
    "Carlos","Victor","Diego","Samuel","Aaron","Eric","Chris","Jamal","Darius",
    "Elijah","Malik","Xavier","Dante","Javier","Marco","Sergio","Luis","Omar",
    "Hassan","Yusuf","Kofi","Emeka","Chidi","Ade","Kwame","Sven","Lars","Otto",
    "Henrik","Klaus","Pieter","Luca","Matteo","Adriano","Esteban","Rodrigo",
]

LAST_NAMES = [
    "Jones","Pereira","Makhachev","Oliveira","Poirier","Gaethje","O'Malley","Topuria",
    "Holloway","Chimaev","McGregor","St-Pierre","Silva","Emelianenko","Aldo","Couture",
    "Lesnar","Velasquez","Cormier","Miocic","Ngannou","Gane","Aspinall","Pimblett",
    "Thompson","Whittaker","Adesanya","Costa","Romero","Blachowicz","Rakic","Prochazka",
    "Teixeira","Machida","Evans","Jackson","Henderson","Fitch","Diaz","Masvidal",
    "Edwards","Covington","Burns","Usman","Woodley","Lawler","Hendricks","Condit",
    "Cerrone","Ferguson","Chandler","Hooker","Moicano","Volkanovski","Ortega","Stephens",
    "Yan","Sandhagen","Sterling","Dillashaw","Faber","Cruz","Moreno","Figueredo",
    "Tuivasa","Volkov","Blaydes","Rozenstruik","Overeem","Hunt","dos Santos",
    "Weidman","Rockhold","Bisping","Gastelum","Brunson","Strickland","du Plessis",
    "Vettori","Imavov","Dariush","Tsarukyan","Allen","Emmett","Kattar",
    "Rakhmonov","Neal","Price","Fiziev","Gamrot","Hardy","Nelson","Belfort",
    "Lombard","Boetsch","Okami","Kennedy","Souza","Till","Reyes","Cannonier",
    "Hermansson","Spann","Santos","Smith","Ankalaev","Gustafsson","Walker",
    "Pavlovich","Spivak","Tybura","Arlovski","Barnett","Nogueira","Werdum",
    "Shogun","Lins","Nzechukwu","Cutelaba","Sanchez","Barboza","Felder",
    "Riddell","Dolidze","Ige","Swanson","Burgos","Iaquinta",
    "Pantoja","Moraes","Erceg","Sahakyan",
    "Nurmagomedov","Khasbulaev","Khizriev","Aliev","Ismailov","Evloev","Musaev",
    "Kim","Park","Lee","Jung","Choi","Cho","Han","Yoo","Oh","Na","Shin",
    "Gomi","Sakurai","Akiyama","Sakuraba","Arona","Phan","Pettis","Lauzon",
    "Lamas","Bermudez","Means","Pearce","Hall","Cummins",
    "Munoz","Philippou","Natal","Tavares","Branch","Camur",
    "Turman","Dober","Puelles","Cejudo","Benavidez","Dodson",
    "Cooper","Walsh","Santos","Rivera","Hayes","Cross","Monroe","Mendoza","Petrov","King",
    "Richards","Turner","Brooks","Wallace","Griffin","Coleman","Dixon","Webb","Hart",
    "Cruz","Reyes","Vargas","Torres","Rojas","Medina","Guerrero","Castillo","Herrera",
    "Ivanov","Volkov","Sidorov","Petrov","Kozlov","Morozov","Novikov","Fedorov",
]

NICKNAMES = [
    "The Predator","Iron","The Nightmare","Notorious","The Eagle","Bones",
    "Stylebender","The Spider","The Natural","The Iceman","Ruthless","Gamebred",
    "The Immortal","Rampage","Lionheart","The Assassin","Chaos","The Eraser",
    "The Machine","Vicious","The Hurricane","El Cucuy","The Diamond","Blessed",
    "The Highlight","The Phenom","Wolverine","The Reaper","The King","War",
    "The Polish Power","The Juggernaut","Pitbull","The Axe Murderer","The Dragon",
    "The Underground King","The Dark Knight","El Matador","Showtime",
    "The American Gangster","The Chosen One","Lightning","The Carpenter",
    "Thundercat","The Answer","Bam Bam","The Ghost","The Prodigy",
    "Hardcore","The Wisconsin Viking","The Count","Crazy Horse",
    "The Doberman","Tarzan","The Viking","The Muscle Shark",
    "Black Beast","The Destroyer","Bullet","Thug","The Terror",
    "El Guapo","The Spartan","The Renegade","The Butcher","Overtime",
    "The Savage","The Animal","The Wolf","The Bear","The Cobra",
    "The Sniper","The Hitman","The Surgeon","The Executioner",
    "The Punisher","The Beast","The Gladiator","Silverback","Showstopper",
    "El Toro","The Freight Train","Silent Assassin","The Technician",
    "Mr. Perfect","The Professor","Ground Zero","The Closer","The Finisher",
    "The Jackhammer","The Wrecking Ball","The Buzzsaw","Hands of Stone",
    "The Mongoose","The Python","The Titan","The Warrior","The Conqueror",
    "The Archangel","The Alligator","The Pirate","The Terminator",
    "Mad Dog","The Ironman","The Undertaker","Nuclear","The Razor",
    "The Hurricane","The Warlord","Lights Out",
    "Rocky","The Bull","The Hammer","Cold Steel","The Outlaw","Platinum",
    "The Ninja","The Centurion","The Blaze","El Desperado","The Storm",
    "El Rayo","Iron Will","The Legend","The Showman","The Wildcard","The Entertainer",
]

PERSONALITIES = [
    "Aggressive","Technical","Wild","Calculated","Composed","Reckless",
    "Methodical","Explosive","Patient","Ferocious","Cerebral","Relentless",
]

PAST_PROMOTIONS = [
    "ISKA World","Bellator","ONE Championship","Strikeforce","WSOF",
    "PFL","LFA","RFA","ACB","M-1 Global","XFC","CES MMA","Ring of Combat",
    "Titan FC","Cage Warriors","BAMMA","Brave CF","KSW","ROAD FC",
]

PRIOR_TITLES = [
    "Olympic Wrestling Bronze Medalist","World Judo Champion",
    "Brazilian Jiu-Jitsu World Champion","ADCC Submission Wrestling Gold",
    "K-1 World Grand Prix Winner","National Muay Thai Champion",
    "NCAA Division I Wrestling Champion","World Sambo Champion",
    "World Boxing Council Super-Featherweight Champion",
    "Regional Golden Gloves Champion","Amateur MMA World Title",
    "Invicta FC Champion (contested internationally)",
    "National Kickboxing Federation Champion","IMMAF World Gold Medalist",
    "Pankration World Champion","National Greco-Roman Wrestling Title",
]

# ─── COMMENTARY DATABASE ───────────────────────────────────────────────────────
COMMENTARY = {
    "light_strike": [
        "{att} probes with a quick jab, feeling out the range.",
        "{att} lands a leg kick to the lead thigh.",
        "{att} touches {defender} with a check hook.",
        "{att} goes to the body with a straight left.",
        "{att} snaps {defender}'s head back with a sharp jab.",
        "{att} feints high then digs a short right to the body.",
        "{att} lands a crisp inside low kick, checking {defender}'s stance.",
        "{att} pops a jab off the nose of {defender} — clean but light.",
    ],
    "light_strike_Striker": [
        "{att} flicks a razor-sharp jab that snaps {defender}'s head.",
        "{att} throws a textbook 1-2, both punches landing clean.",
        "{att} times {defender} stepping in with a check hook.",
        "{att} digs a crisp left hook to the liver — {defender} grimaces.",
        "{att} fires a teep that stops {defender}'s advance cold.",
        "{att} dances outside and pops a jab off the nose.",
        "{att} uses lateral movement to create the angle, fires a right cross.",
        "{att} catches {defender} coming forward with a stiff counter jab.",
    ],
    "light_strike_Grappler": [
        "{att} throws a short right hand to set up the clinch.",
        "{att} lands a looping overhand while closing the distance.",
        "{att} catches {defender} with an inside low kick before tying up.",
        "{att} lands a short uppercut in the pocket, then grabs a tie.",
        "{att} presses {defender} against the cage and lands short knees.",
    ],
    "light_strike_Brawler": [
        "{att} swings a wide left hook that grazes {defender}'s chin.",
        "{att} lobs a slow overhand right — {defender} partially slips it.",
        "{att} lunges in with a looping body shot that partially lands.",
        "{att} plods forward and lands a meaty body blow.",
        "{att} cracks a wild overhand that clips {defender} on the ear.",
    ],
    "heavy_strike": [
        "{att} LANDS A HUGE OVERHAND RIGHT — {defender} is rocked!",
        "{att} connects with a spinning back kick flush to the gut!",
        "{att} rocks {defender} with a flying knee to the face!",
        "{att} lands a crisp 1-2 combo that wobbles {defender}!",
        "{att} cracks {defender} with a head kick — legs go rubbery!",
        "{att} LANDS a brutal right hook — {defender} stumbles sideways!",
        "{att} digs a vicious uppercut that snaps {defender}'s head up!",
    ],
    "heavy_strike_Striker": [
        "{att} DETONATES a left hook on the chin — {defender} staggers!",
        "{att} drops a vicious right hand — {defender}'s mouthguard flies!",
        "{att} lands a head kick — {defender} stumbles into the fence!",
        "{att} fires a four-punch combo — last shot snaps {defender}'s head!",
        "{att} fakes low and uncorks an uppercut — {defender}'s head flies!",
        "{att} lands a spinning back fist — {defender} drops to a knee!",
        "{att} times the counter perfectly — a RIGHT HAND DOWN THE PIPE!",
    ],
    "heavy_strike_Grappler": [
        "{att} clinches and drives a short elbow into {defender}'s temple!",
        "{att} catches {defender}'s kick and hurls them, lands a hammerfist!",
        "{att} lands a brutal knee in the clinch — {defender} bends over!",
        "{att} releases the clinch and smashes a right behind {defender}'s ear!",
        "{att} traps {defender} on the cage and lands a crushing short elbow!",
    ],
    "heavy_strike_Brawler": [
        "{att} BOMBS a wild overhand right — {defender} staggers badly!",
        "{att} charges swinging — a looping left finds the jaw! {defender} DROPS!",
        "{att} uncorks a thunderous uppercut — {defender}'s head snaps back!",
        "{att} launches a flying knee — catches {defender} clean in the face!",
        "{att} fires a haymaker with everything behind it — {defender} crashes!",
        "{att} BOMBS a right hand that sends {defender} stumbling to the fence!",
    ],
    "miss": [
        "{att} swings wildly and hits nothing but air.",
        "{defender} slips the punch smoothly and circles to safety.",
        "{att} throws a haymaker but {defender} ducks under it.",
        "{defender} checks the leg kick hard — {att} hops back.",
        "{att} reaches but {defender} is already gone, circling away.",
    ],
    "miss_Striker": [
        "{defender} reads the combo and slips outside — {att} out of position.",
        "{att} throws a flashy heel kick but {defender} steps back easily.",
        "{att} fires a jab-cross but {defender} rolls under and resets.",
        "{defender} pulls off the line — {att} misses badly.",
        "{att} telegraphs the head kick — {defender} ducks beneath it.",
    ],
    "miss_Grappler": [
        "{att} telegraphs the shot — {defender} sprawls and stuffs it.",
        "{att} reaches for the clinch but {defender} shoves them off.",
        "{att} throws an awkward overhand but {defender} ducks under.",
        "{att} dives for the takedown but {defender} circles away cleanly.",
    ],
    "miss_Brawler": [
        "{att} windmills a wild right and nearly spins off balance.",
        "{defender} steps inside the wild swing — {att}'s momentum carries past.",
        "{att} lunges with both hands swinging but {defender} isn't there.",
        "{att} charges in recklessly and eats a sharp jab counter.",
        "{att} overcommits to a haymaker — falls short by half a foot.",
    ],
    "cut_opened": [
        "A sharp elbow from {att} slices open {defender}'s eyebrow — blood trickles.",
        "{att}'s right hand splits the skin above {defender}'s eye — clean and deep.",
        "A thumb finds {defender}'s eye — ref waves off to check the cut.",
        "{att}'s elbow scythes across {defender}'s cheekbone — nasty gash opens.",
        "{att} digs a right to the nose bridge — blood flows freely.",
        "A clash of heads opens a cut above {defender}'s brow — ref steps in briefly.",
        "{att}'s elbow catches the orbital — a thin red line spreads rapidly.",
    ],
    "cut_worsened": [
        "Blood streaming into {defender}'s eyes — fighting half-blind.",
        "Ref calls time — doctor inspects the deepening cut on {defender}.",
        "{att} notices the blood and goes right back at the cut with an elbow.",
        "{defender}'s cut opens wider — the mat spots red beneath them.",
        "The ringside physician is concerned — {defender}'s cut is worsening badly.",
    ],
    "injury_body": [
        "{att} digs a savage hook to the ribs — {defender} grunts audibly.",
        "{att} hammers the body — {defender} moves stiffly, guarding the ribs.",
        "A left hook to the liver from {att} buckles {defender}'s knees.",
        "{defender} winces as {att}'s body shot crunches the side — rib injury.",
        "{att} drives a short knee to the midsection — {defender} doubles over.",
        "{att}'s body kick lands with a sickening crack — that sounded like a rib.",
    ],
    "injury_eye": [
        "A head clash leaves {defender} with a swelling eye — purple and puffy.",
        "{defender}'s eye is nearly swollen shut — can barely track {att}.",
        "{att}'s jab repeatedly finds the same spot — it's swelling badly.",
        "Doctor examines {defender}'s eye between rounds — close to stoppage.",
        "{att}'s thumb rakes across {defender}'s eye — vision clearly impaired.",
    ],
    "injury_nose": [
        "{att}'s right hand lands flush — {defender}'s face erupts in blood.",
        "A cracking jab from {att} visibly bends {defender}'s nose sideways.",
        "{defender}'s nose is clearly broken — crimson streams down the chin.",
        "{att} lands an elbow that smashes the cartilage in {defender}'s nose.",
        "{att}'s straight right smashes the nose — {defender} gasps, face a mess.",
    ],
    "takedown_success": [
        "{att} BLASTS a double-leg, driving {defender} to the mat hard!",
        "{att} trips {defender} from the clinch, lands in top control.",
        "{att} catches a kick and sweeps {defender} off their feet.",
        "{att} shoots a slick single-leg and drags {defender} down.",
        "{att} trips the inside leg — {defender} hits the canvas face-first!",
    ],
    "takedown_success_Grappler": [
        "{att} times the level change — textbook double-leg, {defender} SLAMMED!",
        "{att} works a body lock — executes a perfect suplex, {defender} crashes!",
        "{att} trips the far leg, transitions to back control seamlessly.",
        "{att} feints the jab and snaps down a lightning-fast low single.",
        "{att} drags {defender} from the Thai plum — immediately takes mount.",
        "{att} lifts {defender} overhead and SLAMS them to the mat with authority!",
    ],
    "takedown_fail": [
        "{att} shoots but {defender} sprawls heavily, stuffing the attempt.",
        "{att} tries a hip throw but {defender} bases out and stays up.",
        "{att} reaches for a single-leg but {defender} hops free.",
        "{defender} catches the attempt and shoves {att} away aggressively.",
        "{att} telegraphs the shot — {defender} stuffs the head and resets.",
    ],
    "ground_pound": [
        "{att} postures up from mount and rains down hammerfists!",
        "{att} passes to side control and drops sharp elbows on {defender}!",
        "{att} works from half-guard, landing short punches to ribs and temple.",
        "{att} drives a vicious short elbow into {defender}'s skull from top!",
        "{att} takes the back, lands hard short rights to the temple of {defender}!",
    ],
    "ground_pound_Grappler": [
        "{att} takes the back — sinks a rear naked choke — {defender} fighting!",
        "{att} locks up an arm bar from mount — {defender} frantically rolls.",
        "{att} works a D'arce choke — {defender} is going purple!",
        "{att} transitions from mount to back control — {defender} can't keep up.",
        "{att} floats to mount and postures up — {defender} shell-shocked below!",
    ],
    "ground_idle": [
        "{att} controls the wrists methodically, neutralising {defender}'s offence.",
        "{defender} hugs tight, trying to weather the storm and wait for standup.",
        "Both fighters catch their breath on the mat. The crowd grows restless.",
        "{defender} turns away — the ref warns them to be active.",
        "{att} holds top position but can't advance — {defender} ties them up.",
        "The clinch work continues — neither fighter able to impose their game.",
    ],
    "critical_health": [
        "{defender} is HURT — {att} smells blood and swarms!",
        "{defender} is in deep trouble — stumbling on rubber legs!",
        "{att} is relentless — {defender} barely surviving on instinct alone!",
        "{defender}'s corner is screaming — their fighter is fading fast!",
        "Is this the end? {defender} is barely staying upright!",
    ],
    "late_round": [
        "Championship rounds — this is where legends are made.",
        "Exhaustion has set in — both fighters running on pure heart.",
        "{att} digging deep into reserves — every punch costing energy.",
        "The crowd roars — they know they're watching something special.",
        "Third round — the judges' scorecards will decide if this goes the distance.",
    ],
    "dominant_run": [
        "{att} has been imposing their will all round — {defender} needs a miracle.",
        "{att} is outclassing {defender} in every area of this fight.",
        "Total domination by {att} — {defender} can't find their rhythm.",
    ],
}

# ─── VISUAL SYSTEM ──────────────────────────────────────────────────────────────
if os.name == 'nt': os.system('')
CR='\033[91m'; CB='\033[94m'; CG='\033[92m'; CY='\033[93m'
CC='\033[96m'; CW='\033[97m'; CM='\033[95m'; DIM='\033[2m'
BLD='\033[1m'; RST='\033[0m'
TW = 78

def _vis(s):   return len(re.sub(r'\033\[[0-9;]*m','',s))
def _pr(s, w): return s + ' '*max(0,w-_vis(s))
def _pl(s, w): return ' '*max(0,w-_vis(s)) + s
def _pc(s, w):
    p = max(0,w-_vis(s)); return ' '*(p//2)+s+' '*(p-p//2)

def clear_screen(): os.system('cls' if os.name == 'nt' else 'clear')

def draw_header(title, game=None):
    clear_screen()
    ds = f"WEEK {game.week}, {game.year} " if game else ""
    t  = f"{BLD}{CY} \u2605 {CW}{title.upper()}{CY} \u2605{RST}"
    pad = TW-2-_vis(t)-len(ds)
    print(f"{CY}\u2554{'═'*(TW-2)}\u2557{RST}")
    print(f"{CY}\u2551{RST}{t}{' '*max(1,pad)}{DIM}{ds}{RST}{CY}\u2551{RST}")
    print(f"{CY}\u2560{'═'*(TW-2)}\u2563{RST}")

def draw_bar(cur, maxv, length=16):
    pct=max(0,min(1.0,cur/maxv)); f=int(length*pct); p=int(pct*100)
    col=CG if p>60 else CY if p>30 else CR
    return f"{col}{'█'*f}{DIM}{'░'*(length-f)}{RST} {CW}{p:3d}%{RST}"

def draw_prog_bar(pct, length=18, broken=False):
    """Generic progress bar toward a target. pct = 0.0-1.0."""
    filled = int(length * min(1.0, pct))
    if broken:   col = CG
    elif pct > 0.66: col = CY
    elif pct > 0.33: col = CC
    elif pct > 0:    col = DIM
    else:            col = DIM
    return f"[{col}{'█'*filled}{DIM}{'░'*(length-filled)}{RST}]"

def fame_bar(fame, length=10):
    f=int(length*fame/100)
    return f"{CM}{'★'*f}{DIM}{'·'*(length-f)}{RST} {CW}{fame:>3}{RST}"

def _fbar_l(val, blen=12):
    pct=max(0,min(1.0,val/100)); f,n=int(blen*pct),int(pct*100)
    col=CG if n>60 else CY if n>30 else CR
    return f" {CW}{n:3d}%{RST} {col}{'█'*f}{DIM}{'░'*(blen-f)}{RST} "

def _fbar_r(val, blen=12):
    pct=max(0,min(1.0,val/100)); f,n=int(blen*pct),int(pct*100)
    col=CG if n>60 else CY if n>30 else CR
    return f" {DIM}{'░'*(blen-f)}{RST}{col}{'█'*f}{RST} {CW}{n:3d}%{RST} "

def generate_name(): return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

def _wrap(text, width):
    words,lines,line = text.split(),[],""
    for w in words:
        if len(line)+len(w)+(1 if line else 0)<=width: line+=(" " if line else "")+w
        else:
            if line: lines.append(line)
            line=w
    if line: lines.append(line)
    return lines or [""]

def _news_color(item):
    """Return color code for a news item based on its prefix tag."""
    if item.startswith("[!]") or item.startswith("UPSET"):   return CR
    if item.startswith("[★]") or item.startswith("CHAMPION"): return CY
    if item.startswith("[*]") or item.startswith("DOMINANT"): return CC
    if item.startswith("[v]") or item.startswith("SKID"):     return DIM
    if item.startswith("RESULT") or item.startswith("[>]"):   return CG
    if item.startswith("RECORD"):                             return CM
    if item.startswith("FIGHT BOOKED"):                      return CB
    return DIM

# ─── SAVE SYSTEM ─────────────────────────────────────────────────────────────────
def _save_path():
    if getattr(sys,'frozen',False):
        return pathlib.Path(sys.executable).parent / "mma_save.pkl"
    return pathlib.Path(__file__).parent / "mma_save.pkl"

def save_game(game):
    try:
        with open(_save_path(),'wb') as f: pickle.dump(game,f)
        return True
    except Exception:
        return False

def load_game():
    p = _save_path()
    if not p.exists(): return None
    try:
        with open(p,'rb') as f: return pickle.load(f)
    except Exception:
        return None

def delete_save():
    p = _save_path()
    if p.exists():
        try: p.unlink()
        except Exception: pass

# ─── TRAINING CAMP OPTIONS ─────────────────────────────────────────────────────
CAMP_DRILLS = [
    ("S","Striking Drills",  2000,20,"striking", 1,3,"Punching & kicking technique"),
    ("G","Grappling Clinic", 2000,20,"grappling",1,3,"Wrestling, judo & submissions"),
    ("D","Defense Workshop", 1500,20,"defense",  1,3,"Head movement, blocks & footwork"),
    ("C","Conditioning Run", 1000,15,"stamina",  1,3,"Cardio & aerobic base"),
    ("P","Power & Strength", 1500,25,"strength", 1,3,"Heavy lifting & explosiveness"),
    ("T","Toughness Camp",   1500,20,"toughness",1,3,"Chin conditioning & body hardening"),
    ("W","Sparring Session", 3000,35,"all",      1,1,"All stats +1, high cost"),
    ("R","Rest Day",            0,-30,"rest",    0,0,"Recover 30 stamina, free"),
]

# ─── FIGHTER CLASS ──────────────────────────────────────────────────────────────
class Fighter:
    STYLES = ["Striker","Grappler","Brawler","Balanced"]

    def __init__(self, name, age, style, weight_class, cost=0, is_player=False):
        self.name           = name
        self.age            = age
        self.style          = style
        self.weight_class   = weight_class
        self.record         = {"W":0,"L":0,"D":0}
        self.is_player      = is_player
        self.contract_value = cost

        self.stamina   = random.randint(60,95)
        self.toughness = random.randint(60,95)
        self.strength  = random.randint(50,95)
        self.striking  = random.randint(40,90)
        self.grappling = random.randint(40,90)
        self.defense   = random.randint(40,90)

        self.weekly_stamina = 100
        self.health=100.0; self.energy=100.0
        self.is_knocked_out=False
        self.stats={"Landed":0,"Thrown":0,"Takedowns":0,"Damage":0}

        self.nickname     = None
        self.personality  = random.choice(PERSONALITIES)
        self.cuts         = 0
        self.injury       = None
        self.fame         = 0
        self.win_streak   = 0
        self.loss_streak  = 0
        self.career_kos   = 0
        self.peak_rank    = 999
        self.achievements = []
        self.fight_history= []
        self.god_mode     = False

    def _log_fight(self, opponent_name, result, method, rnd, week, year):
        self.fight_history.append({
            "opponent": opponent_name, "result": result,
            "method": method, "round": rnd, "week": week, "year": year,
        })
        if len(self.fight_history) > 10: self.fight_history.pop(0)

    def add_win(self, by_finish=False):
        self.record["W"]+=1; self.win_streak+=1; self.loss_streak=0
        if by_finish: self.career_kos+=1
        gain=5+(3 if self.win_streak>=3 else 0)+(2 if by_finish else 0)
        self.fame=min(100,self.fame+gain)
        if random.random()<0.35:
            attr=random.choice(["striking","grappling","defense","stamina"])
            setattr(self,attr,min(99,getattr(self,attr)+1))

    def add_loss(self, by_finish=False):
        self.record["L"]+=1; self.loss_streak+=1; self.win_streak=0
        lose=3+(4 if self.loss_streak>=2 else 0)+(2 if by_finish else 0)
        self.fame=max(0,self.fame-lose)
        if self.loss_streak>=2:
            attr=random.choice(["striking","grappling","defense"])
            setattr(self,attr,max(20,getattr(self,attr)-1))

    def grant_achievement(self, text):
        if text not in self.achievements:
            self.achievements.append(text)

    def calc_purse(self, fight_type):
        fm=max(0.3,0.5+self.fame/100)
        if   fight_type=="championship": base=random.randint(120_000,400_000)
        elif fight_type=="contender":    base=random.randint(50_000, 150_000)
        elif fight_type=="ranked":       base=random.randint(15_000,  50_000)
        else:                            base=random.randint( 3_000,  12_000)
        return int(base*fm)

    def do_drill(self, drill_key, game):
        d=next((x for x in CAMP_DRILLS if x[0]==drill_key),None)
        if not d: return False,"  Unknown drill."
        key,label,cost,stam,stat,lo,hi,_ = d
        if stat=="rest":
            self.weekly_stamina=min(100,self.weekly_stamina+30)
            return True,f"  {CG}Rest complete. Stamina recovered.{RST}"
        if self.weekly_stamina<stam:
            return False,f"  {CR}Not enough camp stamina ({self.weekly_stamina}/{stam}).{RST}"
        if game.funds<cost:
            return False,f"  {CR}Insufficient funds (need ${cost:,}).{RST}"
        self.weekly_stamina-=stam; game.funds-=cost
        if stat=="all":
            for s in ("striking","grappling","defense","stamina","strength","toughness"):
                setattr(self,s,min(99,getattr(self,s)+1))
            return True,f"  {CG}Sparring done! All stats +1.{RST}"
        inc=random.randint(lo,hi)
        setattr(self,stat,min(99,getattr(self,stat)+inc))
        return True,f"  {CG}{label} complete! {stat.capitalize()} +{inc}.{RST}"

    def reset_for_fight(self):
        self.health=100.0; self.energy=100.0; self.is_knocked_out=False
        self.stats={"Landed":0,"Thrown":0,"Takedowns":0,"Damage":0}
        self.cuts=0; self.injury=None

    def take_damage(self, amount):
        if getattr(self,'god_mode',False): return  # CHEAT: invincible
        m=amount*(1-self.toughness/300)
        self.health-=m
        if self.health<=0: self.health=0; self.is_knocked_out=True

    def apply_cut(self, sev=1):
        if getattr(self,'god_mode',False): return False  # CHEAT
        self.cuts=min(3,self.cuts+sev)
        if self.cuts>=3: self.is_knocked_out=True; return True
        return False

    def apply_injury(self, t):
        self.injury=t
        if t=="Rib":  self.defense =max(1,self.defense -10)
        elif t=="Eye": self.striking=max(1,self.striking-8)
        elif t=="Nose":self.defense =max(1,self.defense -5)

    @property
    def display_name(self):
        return f"{self.name} \"{self.nickname}\"" if self.nickname else self.name

    @property
    def streak_str(self):
        if self.win_streak>=2:  return f"{CG}W{self.win_streak}{RST}"
        if self.loss_streak>=2: return f"{CR}L{self.loss_streak}{RST}"
        return f"{DIM}—{RST}"

# ─── GAME STATE ─────────────────────────────────────────────────────────────────
class GameState:
    def __init__(self):
        self.funds=500_000; self.week=1; self.year=2024
        self.gym_roster=[]; self.news_feed=["Welcome to MMA Legends. Build your dynasty."]
        self.world_roster={}; self.scheduled_fight=None; self.total_income=0
        self.generate_world()
        # Records: each has current holder + val, and a legendary TARGET to chase
        self.records={
            "Fastest KO":{
                "holder":"—","val":999,"sfx":"s",
                "target_val":9,"target_holder":"Julio 'El Rayo' Mendoza",
                "lower_better":True,"desc":"Fastest finish ever recorded"
            },
            "Most Damage (Fight)":{
                "holder":"—","val":0,"sfx":"",
                "target_val":280,"target_holder":"Mike 'The Destroyer' Walsh",
                "lower_better":False,"desc":"Most damage dealt in one fight"
            },
            "Most TDs (Fight)":{
                "holder":"—","val":0,"sfx":"",
                "target_val":12,"target_holder":"Viktor 'The Bear' Petrov",
                "lower_better":False,"desc":"Most takedowns in one fight"
            },
            "Longest Win Streak":{
                "holder":"—","val":0,"sfx":"",
                "target_val":15,"target_holder":"Danny 'Iron Will' Santos",
                "lower_better":False,"desc":"Most consecutive victories"
            },
            "Most Career Wins":{
                "holder":"—","val":0,"sfx":"",
                "target_val":30,"target_holder":"James 'The Legend' Cooper",
                "lower_better":False,"desc":"Most wins over a career"
            },
            "Most Career KOs":{
                "holder":"—","val":0,"sfx":"",
                "target_val":20,"target_holder":"Marcus 'Lights Out' King",
                "lower_better":False,"desc":"Most career finishes"
            },
            "Biggest Upset (Rnk)":{
                "holder":"—","val":0,"sfx":" spots",
                "target_val":13,"target_holder":"Bobby 'Wildcard' Hayes",
                "lower_better":False,"desc":"Biggest ranked upset in history"
            },
            "Highest Fame":{
                "holder":"—","val":0,"sfx":"/100",
                "target_val":97,"target_holder":"Carlos 'The Showman' Rivera",
                "lower_better":False,"desc":"Peak fame ever achieved"
            },
            "Most Win Bonuses":{
                "holder":"—","val":0,"sfx":"",
                "target_val":16,"target_holder":"Eddie 'The Entertainer' Cross",
                "lower_better":False,"desc":"Most performance bonuses earned"
            },
            "Richest Manager":{
                "holder":"—","val":0,"sfx":"",
                "currency":True,
                "target_val":12_000_000,"target_holder":"Dynasty Sports Management",
                "lower_better":False,"desc":"Total career manager earnings"
            },
        }
        self.hall_of_fame=[
            {"name":"Anderson Silva",     "reason":"16-fight UFC winning streak — legendary Striker"},
            {"name":"GSP",                "reason":"Welterweight GOAT — 12 dominant title defenses"},
            {"name":"Fedor Emelianenko",  "reason":"Greatest HW of all time — 28-fight unbeaten run"},
            {"name":"Demetrious Johnson", "reason":"Most UFC title defenses in history — 11 straight"},
        ]
        self.total_bonuses=0

    # ── Record update helper ──────────────────────────────────────────────────
    def _update_rec(self, key, holder, val):
        """Update only holder/val of a record, preserving target fields."""
        if key in self.records:
            self.records[key]["holder"] = holder
            self.records[key]["val"]    = val

    # ── World generation ──────────────────────────────────────────────────────
    def generate_world(self):
        print(f"{CY}Generating Global Roster...{RST}")
        used_nicks=set()
        for wc in MEN_WEIGHT_CLASSES:
            roster=[]
            for i in range(46):
                f=Fighter(generate_name(),random.randint(22,38),
                          random.choice(Fighter.STYLES),wc)
                bonus=max(0,40-i)
                f.striking=min(99,f.striking+bonus)
                f.grappling=min(99,f.grappling+bonus)
                if random.random()<0.70:
                    avail=[n for n in NICKNAMES if n not in used_nicks]
                    if avail:
                        nick=random.choice(avail)
                        f.nickname=nick; used_nicks.add(nick)
                roster.append(f)
            self.world_roster[wc]=roster
        self.simulate_history()

    def simulate_history(self):
        for wc in MEN_WEIGHT_CLASSES:
            roster=self.world_roster[wc]
            for rank_idx,f in enumerate(roster):
                if f.is_player: continue
                rf=max(0.0,1.0-rank_idx/len(roster))
                fights=random.randint(4,int(8+rf*22))
                wr=0.35+rf*0.55
                for _ in range(fights):
                    r=random.random()
                    if r<wr:        f.add_win(by_finish=random.random()<0.30)
                    elif r<wr+0.025:f.record["D"]+=1
                    else:           f.add_loss(by_finish=random.random()<0.25)
                f.fame=max(0,min(100,int(rf*80)+random.randint(-10,10)))
                if rank_idx==0:
                    promo=random.choice(PAST_PROMOTIONS)
                    f.grant_achievement(f"Former {promo} Champion")
                    f.grant_achievement(f"Title defended {random.randint(1,4)} times")
                elif rank_idx<=5:
                    if random.random()<0.5:
                        promo=random.choice(PAST_PROMOTIONS)
                        f.grant_achievement(f"Former {promo} Champion")
                if random.random()<0.4:
                    f.grant_achievement(random.choice(PRIOR_TITLES))
                if f.career_kos>=8:
                    f.grant_achievement(f"{f.career_kos} career finishes")
                if f.win_streak>=5:
                    f.grant_achievement(f"Peak {f.win_streak}-fight winning streak")
                opp_pool=self.world_roster.get(wc,[])
                for _ in range(min(5,f.record["W"]+f.record["L"])):
                    opp=random.choice(opp_pool) if opp_pool else None
                    opp_name=opp.name if opp and opp!=f else generate_name()
                    result=random.choices(["W","L"],weights=[wr,1-wr])[0]
                    method=random.choice(["KO/TKO","Decision","Submission"])
                    f.fight_history.append({
                        "opponent":opp_name,"result":result,
                        "method":method,"round":random.randint(1,3),
                        "week":random.randint(1,52),"year":random.randint(2018,2023),
                    })

    # ── Fight type / camp helpers ─────────────────────────────────────────────
    def get_fight_type(self,opp):
        idx=self.get_rank_index(opp)
        if idx==0:  return "championship"
        if idx<=5:  return "contender"
        if idx<=15: return "ranked"
        return "unranked"

    def camp_duration(self,ft):
        if ft=="championship":          return random.randint(8,10)
        if ft in("contender","ranked"): return random.randint(6,8)
        return 4

    def book_fight(self,fighter,opponent):
        ft=self.get_fight_type(opponent); wks=self.camp_duration(ft)
        o_idx=self.get_rank_index(opponent)
        o_rank="C" if o_idx==0 else f"#{o_idx}" if o_idx<=15 else "NR"
        self.scheduled_fight={"fighter":fighter,"opponent":opponent,
                               "fight_type":ft,"weeks_total":wks,"weeks_done":0}
        fighter.weekly_stamina=100
        self.news_feed.insert(0,
            f"FIGHT BOOKED: {fighter.name} vs {opponent.name} ({o_rank}) — {ft.upper()}, {wks}wk camp")
        return ft,wks

    # ── Ranking helpers ───────────────────────────────────────────────────────
    def get_fighter_rank(self,f):
        roster=self.world_roster.get(f.weight_class,[])
        if f in roster:
            idx=roster.index(f)
            if idx==0: return "C"
            if idx<=15:return f"#{idx}"
        return "NR"

    def get_rank_index(self,f):
        roster=self.world_roster.get(f.weight_class,[])
        return roster.index(f) if f in roster else 999

    def update_rank_after_fight(self,winner,loser):
        roster=self.world_roster.get(winner.weight_class,[])
        if winner not in roster or loser not in roster: return False
        w,l=roster.index(winner),roster.index(loser)
        winner.peak_rank=min(winner.peak_rank,min(w,l))
        if w>l: roster.pop(w); roster.insert(l,winner); return True
        return False

    def _ai_rank_update(self,roster,winner,loser):
        if winner not in roster or loser not in roster: return
        w=roster.index(winner); l=roster.index(loser)
        move=min(3,1+winner.win_streak//3)
        nw=max(l if w>l else 0,w-move)
        roster.pop(w); roster.insert(nw,winner)
        l=roster.index(loser)
        drop=min(5,1+max(0,loser.loss_streak-1))
        nl=min(len(roster)-1,l+drop)
        if nl!=l: roster.pop(l); roster.insert(nl,loser)

    def _tick_rec(self,f):
        if f.win_streak>self.records["Longest Win Streak"]["val"]:
            self._update_rec("Longest Win Streak",f.name,f.win_streak)
        if f.record["W"]>self.records["Most Career Wins"]["val"]:
            self._update_rec("Most Career Wins",f.name,f.record["W"])
        if f.career_kos>self.records["Most Career KOs"]["val"]:
            self._update_rec("Most Career KOs",f.name,f.career_kos)
        if f.fame>self.records["Highest Fame"]["val"]:
            self._update_rec("Highest Fame",f.name,f.fame)

    def check_fight_records(self,winner,loser,time_sec,method,wr,lr):
        if method=="KO/TKO" and time_sec<self.records["Fastest KO"]["val"]:
            self._update_rec("Fastest KO",winner.name,time_sec)
            self.news_feed.insert(0,f"RECORD: {winner.name} fastest KO ({time_sec}s)!")
        dmg=winner.stats["Damage"]
        if dmg>self.records["Most Damage (Fight)"]["val"]:
            self._update_rec("Most Damage (Fight)",winner.name,int(dmg))
        td=winner.stats["Takedowns"]
        if td>self.records["Most TDs (Fight)"]["val"]:
            self._update_rec("Most TDs (Fight)",winner.name,td)
        self._tick_rec(winner)
        if wr>lr:
            ud=wr-lr
            if ud>self.records["Biggest Upset (Rnk)"]["val"]:
                self._update_rec("Biggest Upset (Rnk)",winner.name,ud)
        if self.total_bonuses>self.records["Most Win Bonuses"]["val"]:
            self._update_rec("Most Win Bonuses","You (Manager)",self.total_bonuses)
        if self.total_income>self.records["Richest Manager"]["val"]:
            self._update_rec("Richest Manager","You (Manager)",self.total_income)

    # ── Player achievement checker ────────────────────────────────────────────
    def check_player_achievements(self,fighter):
        rank=self.get_rank_index(fighter)
        if fighter.record["W"]==1:
            fighter.grant_achievement("First Professional Win")
        if fighter.record["W"]==5:
            fighter.grant_achievement("5 Career Wins")
        if fighter.record["W"]==10:
            fighter.grant_achievement("10 Career Wins")
        if fighter.career_kos==1:
            fighter.grant_achievement("First Finish Victory")
        if fighter.career_kos==5:
            fighter.grant_achievement("5 Career Finishes")
        if fighter.win_streak==3:
            fighter.grant_achievement("3-Fight Win Streak")
        if fighter.win_streak==5:
            fighter.grant_achievement("5-Fight Win Streak")
        if rank<=15 and "Top 15 Ranked" not in fighter.achievements:
            fighter.grant_achievement("Top 15 Ranked")
        if rank<=5 and "Top 5 Contender" not in fighter.achievements:
            fighter.grant_achievement("Top 5 Contender")
        if rank==0 and "WORLD CHAMPION" not in fighter.achievements:
            fighter.grant_achievement("WORLD CHAMPION")
            wc_short=fighter.weight_class.split("(")[0].strip()
            fighter.grant_achievement(f"{wc_short} Champion")

    # ── World simulation ──────────────────────────────────────────────────────
    def simulate_world(self):
        news=[]
        for _ in range(random.randint(7,12)):
            wc=random.choice(MEN_WEIGHT_CLASSES)
            roster=self.world_roster[wc]
            if len(roster)<4: continue
            idx1=random.randint(0,min(38,len(roster)-2))
            gap=random.randint(1,min(6,len(roster)-idx1-1))
            idx2=idx1+gap
            if idx2>=len(roster): continue
            f1,f2=roster[idx1],roster[idx2]
            if f1.is_player or f2.is_player: continue
            for f in (f1,f2):
                s=random.choice(["striking","grappling","defense"])
                setattr(f,s,min(99,getattr(f,s)+random.randint(0,1)))
            p1=f1.striking+f1.grappling+f1.stamina+f1.fame//5+random.randint(-25,25)
            p2=f2.striking+f2.grappling+f2.stamina+f2.fame//5+random.randint(-25,25)
            winner,loser=(f1,f2) if p1>=p2 else (f2,f1)
            wb=roster.index(winner); lb=roster.index(loser)
            by_fin=random.random()<0.35
            winner.add_win(by_finish=by_fin); loser.add_loss(by_finish=by_fin)
            self._ai_rank_update(roster,winner,loser)
            self._tick_rec(winner)
            is_upset=wb>lb
            wc_short=wc.split("(")[0].strip()
            method=random.choice(["KO/TKO","Decision","Submission"])
            if is_upset:
                ud=wb-lb
                if ud>self.records["Biggest Upset (Rnk)"]["val"]:
                    self._update_rec("Biggest Upset (Rnk)",winner.name,ud)
                news.append(f"[!] UPSET [{wc_short}] {winner.name} def. #{lb} {loser.name} via {method}")
            elif winner.win_streak>=5:
                news.append(f"[*] {winner.name} on {winner.win_streak}-fight streak! {wc_short} title shot looming.")
            elif winner.win_streak>=3:
                news.append(f"[*] {winner.name} wins again ({winner.win_streak} str.) in {wc_short}.")
            if loser.loss_streak>=3:
                news.append(f"[v] SKID: {loser.name} drops {loser.loss_streak} straight — ranked dropped.")
            if roster.index(winner)==0:
                news.append(f"[★] CHAMPION {winner.name} retains the {wc_short} title via {method}!")

        self.news_feed=news+self.news_feed
        if len(self.news_feed)>20: self.news_feed=self.news_feed[:20]

        # Random events
        if random.random()<0.35:
            evts=[
                "[►] Performance bonus announced for last week's best finish.",
                "[►] Contract dispute: Top contender demands higher pay.",
                "[►] Exclusive: Rival promotion makes offer to reigning champion.",
                "[►] Champion hospitalised after brutal sparring session.",
                "[!] Wild press conference — punches thrown, security called.",
                "[►] New drug testing protocol catches former top contender.",
                "[►] International card draws record PPV numbers — profits soar.",
                "[!] Contender calls out champion: 'I'll knock you out in round 1.'",
                "[★] Comeback: Former champion announces return from retirement.",
                "[v] Injury update: Fan favourite expected out 6 months.",
                "[►] Promoter announces 5-fight deal with rising unbeaten prospect.",
                "[!] Gym closed after brawl breaks out during open sparring.",
                "[►] Commission reviews controversial decision from last month.",
                "[►] Fighter accused of tampering with gloves — investigation underway.",
                "[►] Legendary trainer retires — his stable left without a coach.",
                "[★] New title shot announced — main event confirmed for next card.",
                "[►] Sponsor pulls out after fighter's social media controversy.",
                "[!] Heated open workout ends with both teams brawling in the gym.",
            ]
            self.news_feed.append(random.choice(evts))

    def advance_week(self):
        self.week+=1
        for f in self.gym_roster: f.weekly_stamina=100
        self.simulate_world()
        if self.week>52: self.week=1; self.year+=1; self.news_feed.insert(0,"[★] HAPPY NEW YEAR! New season begins.")
        if self.scheduled_fight:
            sf=self.scheduled_fight; sf["weeks_done"]+=1
            sf["fighter"].weekly_stamina=100
            if sf["weeks_done"]>=sf["weeks_total"]: return "FIGHT_TIME"
        return None

    # ── Quick gym stats (for gym screen) ─────────────────────────────────────
    def gym_stats(self):
        total_w=sum(f.record["W"] for f in self.gym_roster)
        total_l=sum(f.record["L"] for f in self.gym_roster)
        total_kos=sum(f.career_kos for f in self.gym_roster)
        best=max(self.gym_roster,key=lambda f:f.fame,default=None)
        return total_w,total_l,total_kos,best

# ─── FIGHT ENGINE ───────────────────────────────────────────────────────────────
class FightManager:
    L,M,R = 22,24,28

    def __init__(self,red,blue,game_state,fight_type="unranked"):
        self.red=red; self.blue=blue; self.game=game_state
        self.fight_type=fight_type
        red.reset_for_fight(); blue.reset_for_fight()
        self.round=1; self.is_grounded=False; self.log=[]; self.total_time=0

    def print_intro(self):
        """Dramatic fight intro screen before the first bell."""
        clear_screen()
        r,b = self.red, self.blue
        ft_label = self.fight_type.upper()
        ft_col = {
            "championship": f"{CR}{BLD}",
            "contender":    f"{CM}{BLD}",
            "ranked":       f"{CY}{BLD}",
            "unranked":     f"{CC}",
        }.get(self.fight_type, CW)

        print(f"{CY}╔{'═'*(TW-2)}╗{RST}")
        print(f"{CY}║{RST}{_pc(f'{DIM}T O N I G H T  \'S  M A I N  E V E N T{RST}',TW-2)}{CY}║{RST}")
        print(f"{CY}╠{'═'*(TW//2-1)}╦{'═'*(TW-TW//2-2)}╣{RST}")

        # Corner labels
        lbl_r = f" {CR}{BLD}RED CORNER{RST}"
        lbl_b = f"{CB}{BLD}BLUE CORNER{RST} "
        print(f"{CY}║{RST}{_pr(lbl_r,TW//2-1)}{CY}║{RST}{_pl(lbl_b,TW-TW//2-2)}{CY}║{RST}")

        # Names
        rn = f" {CR}{BLD}{r.name[:18]}{RST}"
        bn = f"{CB}{BLD}{b.name[:18]}{RST} "
        print(f"{CY}║{RST}{_pr(rn,TW//2-1)}{CY}║{RST}{_pl(bn,TW-TW//2-2)}{CY}║{RST}")

        # Nicknames
        rnk = f' {CY}"{r.nickname}"{RST}' if r.nickname else f" {DIM}no alias{RST}"
        bnk = f'{CY}"{b.nickname}"{RST} ' if b.nickname else f"{DIM}no alias{RST} "
        print(f"{CY}║{RST}{_pr(rnk,TW//2-1)}{CY}║{RST}{_pl(bnk,TW-TW//2-2)}{CY}║{RST}")

        # Records
        rr = f" {DIM}{r.record['W']}-{r.record['L']}-{r.record['D']}{RST}"
        br = f"{DIM}{b.record['W']}-{b.record['L']}-{b.record['D']}{RST} "
        print(f"{CY}║{RST}{_pr(rr,TW//2-1)}{CY}║{RST}{_pl(br,TW-TW//2-2)}{CY}║{RST}")

        # Style / fame
        rs = f" {DIM}{r.style}  Fame:{CM}{r.fame}{RST}"
        bs = f"{DIM}{b.style}  Fame:{CM}{b.fame}{RST} "
        print(f"{CY}║{RST}{_pr(rs,TW//2-1)}{CY}║{RST}{_pl(bs,TW-TW//2-2)}{CY}║{RST}")

        # Fight type banner
        print(f"{CY}╠{'═'*(TW//2-1)}╩{'═'*(TW-TW//2-2)}╣{RST}")
        print(f"{CY}║{RST}{_pc(f'{ft_col} ◈  {ft_label} FIGHT  ◈ {RST}',TW-2)}{CY}║{RST}")
        print(f"{CY}╚{'═'*(TW-2)}╝{RST}")
        print()
        input(f"  {DIM}Press ENTER to start the fight...{RST}")

    def run(self):
        self.print_intro()
        while self.round<=3:
            time_left=18
            while time_left>0:
                self.process_turn()
                self.total_time+=10
                time_left-=1
                self.red.energy =max(0,self.red.energy -0.4)
                self.blue.energy=max(0,self.blue.energy-0.4)
                self.print_ui(time_left)
                if self.red.is_knocked_out:  time.sleep(1.0); return self.end_fight(self.blue,self.red, "KO/TKO")
                if self.blue.is_knocked_out: time.sleep(1.0); return self.end_fight(self.red, self.blue,"KO/TKO")
                time.sleep(1.4)
            self.round+=1; self.is_grounded=False
            self.red.health =min(100,self.red.health +10)
            self.blue.health=min(100,self.blue.health+10)
            self.red.energy =min(100,self.red.energy +25)
            self.blue.energy=min(100,self.blue.energy+25)
            if self.round<=3:
                self.print_ui(0)
                print(f"\n{CY}{'─'*TW}{RST}")
                print(f"  {CW}{BLD}END OF ROUND {self.round-1}{RST}")
                input(f"  {DIM}Press ENTER to start round {self.round}...{RST}")
        return self.decision()

    def _pick(self,sk,bk,att,dfd):
        pool=COMMENTARY.get(sk) or COMMENTARY.get(bk) or ["..."]
        return random.choice(pool).format(att=att.name,defender=dfd.name)

    def _apply_fight_injury(self,att,dfd,heavy):
        if random.random()<(0.28 if heavy else 0.06):
            sev=random.choice([1,1,2]) if heavy else 1
            stopped=dfd.apply_cut(sev)
            key="cut_worsened" if dfd.cuts>1 and not stopped else "cut_opened"
            pool=COMMENTARY.get(key,[])
            if pool: self.log.append(random.choice(pool).format(att=att.name,defender=dfd.name))
        if random.random()<(0.15 if heavy else 0.04) and not dfd.injury:
            inj=random.choice(["Rib","Eye","Nose"]); dfd.apply_injury(inj)
            ik={"Rib":"injury_body","Eye":"injury_eye","Nose":"injury_nose"}.get(inj,"injury_body")
            pool=COMMENTARY.get(ik,[])
            if pool: self.log.append(random.choice(pool).format(att=att.name,defender=dfd.name))

    def process_turn(self):
        roll=random.random()
        att=self.red  if random.random()>0.5 else self.blue
        dfd=self.blue if att==self.red else self.red
        td ={"Grappler":0.26,"Brawler":0.07,"Striker":0.05,"Balanced":0.15}.get(att.style,0.15)
        am ={"Striker":0.08,"Balanced":0.0,"Grappler":-0.05,"Brawler":-0.08}.get(att.style,0.0)

        if min(self.red.health,self.blue.health)<30 and random.random()<0.25:
            pool=COMMENTARY.get("critical_health",[])
            if pool:
                self.log.append(random.choice(pool).format(att=att.name,defender=dfd.name))
                if len(self.log)>8: self.log.pop(0)
                return
        if self.round==3 and random.random()<0.12:
            pool=COMMENTARY.get("late_round",[])
            if pool:
                self.log.append(random.choice(pool).format(att=att.name,defender=dfd.name))
                if len(self.log)>8: self.log.pop(0)
                return

        if self.is_grounded:
            if random.random()<0.20:
                self.is_grounded=False
                self.log.append("Ref stands them up due to inactivity.")
            elif att.grappling>dfd.grappling:
                dmg=random.randint(5,12)
                att.stats["Damage"]+=dmg; att.stats["Landed"]+=1
                dfd.take_damage(dmg)
                self.log.append(self._pick(f"ground_pound_{att.style}","ground_pound",att,dfd))
                self._apply_fight_injury(att,dfd,True)
            else:
                self.log.append(self._pick("ground_idle","ground_idle",att,dfd))
        else:
            if roll<td:
                if att.grappling>dfd.grappling:
                    self.is_grounded=True; att.stats["Takedowns"]+=1
                    self.log.append(self._pick(f"takedown_success_{att.style}","takedown_success",att,dfd))
                else:
                    self.log.append(self._pick("takedown_fail","takedown_fail",att,dfd))
            else:
                att.stats["Thrown"]+=1
                hit=0.4+(att.striking-dfd.defense)/200+am
                if random.random()<hit:
                    crit=random.random()<0.15
                    if crit:
                        dmg=random.randint(15,25)
                        txt=self._pick(f"heavy_strike_{att.style}","heavy_strike",att,dfd)
                    else:
                        dmg=random.randint(3,8)
                        txt=self._pick(f"light_strike_{att.style}","light_strike",att,dfd)
                    dfd.take_damage(dmg); att.stats["Damage"]+=dmg; att.stats["Landed"]+=1
                    self.log.append(txt)
                    self._apply_fight_injury(att,dfd,crit)
                else:
                    self.log.append(self._pick(f"miss_{att.style}","miss",att,dfd))

        if len(self.log)>8: self.log.pop(0)

    def print_ui(self,time_left):
        L,M,R=self.L,self.M,self.R; clear_screen()
        hdr_l=f"{BLD}{CW} \u2605 RINGSIDE \u2605{RST}"
        hdr_r=f"  {DIM}WEEK {self.game.week}, {self.game.year}{RST}  {CY}R{self.round}{RST}  {CW}{time_left*10:>3}s{RST} "
        pad=TW-2-_vis(hdr_l)-_vis(hdr_r)
        print(f"{CY}\u2554{'═'*(TW-2)}\u2557{RST}")
        print(f"{CY}\u2551{RST}{hdr_l}{' '*max(1,pad)}{hdr_r}{CY}\u2551{RST}")
        print(f"{CY}\u2560{'═'*L}\u2566{'═'*M}\u2566{'═'*R}\u2563{RST}")
        r_name=f"{CR}{BLD} \u25a0 {RST}{CR}{self.red.name[:16]}{RST}"
        b_name=f"{CB}{self.blue.name[:16]}{RST}{CB} \u25a0 {RST}"
        mc=CM if self.is_grounded else CC
        ml=f"{mc}{'◼ GROUND' if self.is_grounded else '◻ STANDING'}{RST}"
        print(f"{CY}\u2551{RST}{_pr(r_name,L)}{CY}\u2551{RST}{_pc(ml,M)}{CY}\u2551{RST}{_pl(b_name,R)}{CY}\u2551{RST}")
        print(f"{CY}\u255f{'─'*L}\u256b{'─'*M}\u256b{'─'*R}\u2562{RST}")
        print(f"{CY}\u2551{RST}{_pr(_fbar_l(self.red.health),L)}{CY}\u2551{RST}{_pc(f'{DIM}HEALTH{RST}',M)}{CY}\u2551{RST}{_pl(_fbar_r(self.blue.health),R)}{CY}\u2551{RST}")
        print(f"{CY}\u2551{RST}{_pr(_fbar_l(self.red.energy),L)}{CY}\u2551{RST}{_pc(f'{DIM}ENERGY{RST}',M)}{CY}\u2551{RST}{_pl(_fbar_r(self.blue.energy),R)}{CY}\u2551{RST}")
        print(f"{CY}\u255f{'─'*L}\u256b{'─'*M}\u256b{'─'*R}\u2562{RST}")
        rs=f" Str:{CW}{self.red.stats['Landed']:>2}/{self.red.stats['Thrown']:<2}{RST}  TD:{CW}{self.red.stats['Takedowns']}{RST}"
        bs=f"Str:{CW}{self.blue.stats['Landed']:>2}/{self.blue.stats['Thrown']:<2}{RST}  TD:{CW}{self.blue.stats['Takedowns']}{RST} "
        print(f"{CY}\u2551{RST}{_pr(rs,L)}{CY}\u2551{RST}{_pc(f'{DIM}STRIKES / TDs{RST}',M)}{CY}\u2551{RST}{_pl(bs,R)}{CY}\u2551{RST}")
        rd=_pr(f" Dmg: {CW}{int(self.red.stats['Damage'])}{RST}",L)
        bd=_pl(f"Dmg: {CW}{int(self.blue.stats['Damage'])}{RST} ",R)
        print(f"{CY}\u2551{RST}{rd}{CY}\u2551{RST}{' '*M}{CY}\u2551{RST}{bd}{CY}\u2551{RST}")
        print(f"{CY}\u255f{'─'*L}\u256b{'─'*M}\u256b{'─'*R}\u2562{RST}")
        cl={0:f"{DIM}None{RST}",1:f"{CY}Minor{RST}",2:f"{CR}Bad{RST}",3:f"{CR}{BLD}SEVERE{RST}"}
        rc=f" Cut:{cl.get(self.red.cuts,'?')}  Inj:{CR if self.red.injury else DIM}{self.red.injury or 'None'}{RST}"
        bc=f"Cut:{cl.get(self.blue.cuts,'?')}  Inj:{CR if self.blue.injury else DIM}{self.blue.injury or 'None'}{RST} "
        print(f"{CY}\u2551{RST}{_pr(rc,L)}{CY}\u2551{RST}{_pc(f'{DIM}CUTS / INJURIES{RST}',M)}{CY}\u2551{RST}{_pl(bc,R)}{CY}\u2551{RST}")
        print(f"{CY}\u2560{'═'*(TW-2)}\u2563{RST}")
        ml2=TW-6
        lines=(['','','',''] + self.log)[-4:]
        for line in lines:
            plain=re.sub(r'\033\[[0-9;]*m','',line)
            if len(plain)>ml2: plain=plain[:ml2-1]+'\u2026'
            print(f"{CY}\u2551{RST}  {CC}>{RST} {_pr(plain,TW-6)}{CY}\u2551{RST}")
        print(f"{CY}\u255a{'═'*(TW-2)}\u255d{RST}")

    def end_fight(self,winner,loser,method):
        by_finish=method=="KO/TKO"
        wr=self.game.get_rank_index(winner); lr=self.game.get_rank_index(loser)
        winner.add_win(by_finish=by_finish); loser.add_loss(by_finish=by_finish)
        winner._log_fight(loser.name,"W",method,self.round,self.game.week,self.game.year)
        loser._log_fight(winner.name,"L",method,self.round,self.game.week,self.game.year)
        for f in (winner,loser):
            if f.is_player: self.game.check_player_achievements(f)

        w_purse=winner.calc_purse(self.fight_type)
        l_purse=loser.calc_purse(self.fight_type)//2
        bonus=50_000 if random.random()<0.28 else 0
        if bonus: self.game.total_bonuses+=1

        manager_cut=0
        for f,purse in [(winner,w_purse+bonus),(loser,l_purse)]:
            if f.is_player:
                cut=int(purse*0.20)
                self.game.funds+=cut; self.game.total_income+=cut
                manager_cut+=cut

        ranked_up=self.game.update_rank_after_fight(winner,loser)
        self.game.check_fight_records(winner,loser,self.total_time,method,wr,lr)

        fight_news=[
            f"[>] RESULT: {winner.name} def. {loser.name} via {method} (R{self.round})",
        ]
        if ranked_up: fight_news.append(f"[*] RANK CHANGE: {winner.name} moves up — {winner.weight_class}")
        if bonus:     fight_news.append(f"[★] BONUS: {winner.name} earns extra $50,000!")
        record_news=[n for n in self.game.news_feed if n.startswith("RECORD:")]
        self.game.news_feed=fight_news+record_news

        # ── KO flash ──────────────────────────────────────────────────────────
        clear_screen()
        if method=="KO/TKO":
            for _ in range(2):
                print(f"\n{CR}{'█'*TW}{RST}")
                print(_pc(f"{CR}{BLD}  !!! {loser.name.upper()} IS DOWN !!!  {RST}",TW))
                print(f"{CR}{'█'*TW}{RST}\n"); time.sleep(0.5)
                clear_screen(); time.sleep(0.3)

        print(f"{CY}\u2554{'═'*(TW-2)}\u2557{RST}")
        wl=f"{CW}{BLD}WINNER: {winner.name}{RST}  {DIM}via {method}{RST}"
        print(f"{CY}\u2551{RST} {_pr(wl,TW-3)}{CY}\u2551{RST}")
        st=f"{DIM}Record: {winner.record['W']}-{winner.record['L']}   Streak: {CG}{winner.win_streak}{RST}   Fame: {CM}{winner.fame}/100{RST}"
        print(f"{CY}\u2551{RST} {_pr(st,TW-3)}{CY}\u2551{RST}")
        print(f"{CY}\u2560{'═'*(TW-2)}\u2563{RST}")
        print(f"{CY}\u2551{RST} {_pr(f'{CY}FIGHT PURSES{RST}',TW-3)}{CY}\u2551{RST}")
        wl2=f" {CW}{winner.name:<20}{RST}  Won   {CG}${w_purse:>10,}{RST}  {DIM}(mgr: ${int(w_purse*0.2):,}){RST}"
        ll2=f" {CW}{loser.name:<20}{RST}  Show  {DIM}${l_purse:>10,}{RST}  {DIM}(mgr: ${int(l_purse*0.2):,}){RST}"
        print(f"{CY}\u2551{RST}{_pr(wl2,TW-2)}{CY}\u2551{RST}")
        print(f"{CY}\u2551{RST}{_pr(ll2,TW-2)}{CY}\u2551{RST}")
        if bonus:
            print(f"{CY}\u2551{RST}{_pr(f' {CM}{BLD}PERFORMANCE BONUS +${bonus:,}!{RST}',TW-2)}{CY}\u2551{RST}")
        if manager_cut:
            ml3=f" {CG}Manager cut: +${manager_cut:,}   Total earnings: ${self.game.total_income:,}{RST}"
            print(f"{CY}\u2560{'═'*(TW-2)}\u2563{RST}")
            print(f"{CY}\u2551{RST}{_pr(ml3,TW-2)}{CY}\u2551{RST}")
        if ranked_up:
            print(f"{CY}\u2551{RST}{_pr(f' {CG}[ RANK UP ] {winner.name} climbs the {winner.weight_class} rankings!{RST}',TW-2)}{CY}\u2551{RST}")
        new_achs=[a for a in winner.achievements[-3:]]
        if new_achs:
            print(f"{CY}\u2560{'═'*(TW-2)}\u2563{RST}")
            print(f"{CY}\u2551{RST}{_pr(f' {CY}ACHIEVEMENTS UNLOCKED:{RST}',TW-2)}{CY}\u2551{RST}")
            for a in new_achs:
                print(f"{CY}\u2551{RST}{_pr(f'  {CM}\u2605 {a}{RST}',TW-2)}{CY}\u2551{RST}")
        print(f"{CY}\u255a{'═'*(TW-2)}\u255d{RST}")

        sf=self.game.scheduled_fight
        if sf and sf.get("fighter") in (winner,loser):
            self.game.scheduled_fight=None

        # Auto-save if a player fighter was involved
        if winner.is_player or loser.is_player:
            if save_game(self.game):
                print(f"  {DIM}Game auto-saved.{RST}")
        time.sleep(4)

    def decision(self):
        sr=self.red.stats["Damage"]+self.red.stats["Takedowns"]*10
        sb=self.blue.stats["Damage"]+self.blue.stats["Takedowns"]*10
        clear_screen()
        print(f"{CY}\u2554{'═'*(TW-2)}\u2557{RST}")
        print(f"{CY}\u2551{RST}{_pc(f'{BLD}{CW} JUDGES SCORECARD {RST}',TW-2)}{CY}\u2551{RST}")
        print(f"{CY}\u2560{'═'*(TW-2)}\u2563{RST}"); time.sleep(1)
        print(f"{CY}\u2551{RST}{_pr(f'  {CR}{BLD}{self.red.name:<22}{RST}  {DIM}........{RST}  {CW}{int(sr)}{RST}',TW-2)}{CY}\u2551{RST}")
        print(f"{CY}\u2551{RST}{_pr(f'  {CB}{BLD}{self.blue.name:<22}{RST}  {DIM}........{RST}  {CW}{int(sb)}{RST}',TW-2)}{CY}\u2551{RST}")
        print(f"{CY}\u255a{'═'*(TW-2)}\u255d{RST}\n")
        if   sr>sb: self.end_fight(self.red, self.blue,"Decision")
        elif sb>sr: self.end_fight(self.blue,self.red, "Decision")
        else:
            print(f"  {CY}{BLD}DRAW!{RST}")
            self.red.record["D"]+=1; self.blue.record["D"]+=1
        time.sleep(3)

# ─── MENUS ──────────────────────────────────────────────────────────────────────

def menu_title_screen():
    """Splash screen shown at startup. Returns loaded GameState or None for new game."""
    existing = load_game()
    clear_screen()

    # ── Logo box ──────────────────────────────────────────────────────────────
    print(f"{CY}╔{'═'*(TW-2)}╗{RST}")
    print(f"{CY}║{RST}{' '*(TW-2)}{CY}║{RST}")
    logo_lines = [
        f"{CR}{BLD} ░▒▓ {CW}MMA LEGENDS PRO{CR} ▓▒░ {RST}",
        f"{DIM}{'─'*38}{RST}",
        f"{CY}Build Your Dynasty  ·  Claim The Belt  ·  Leave A Legacy{RST}",
        f"{DIM}{'─'*38}{RST}",
    ]
    for line in logo_lines:
        print(f"{CY}║{RST}{_pc(line,TW-2)}{CY}║{RST}")
    print(f"{CY}║{RST}{' '*(TW-2)}{CY}║{RST}")
    print(f"{CY}╠{'═'*(TW-2)}╣{RST}")

    # ── Save info ─────────────────────────────────────────────────────────────
    if existing:
        gw=existing.week; gy=existing.year
        gf=f"${existing.funds:,}"; gfighters=len(existing.gym_roster)
        best_rank="NR"
        for f in existing.gym_roster:
            r=existing.get_fighter_rank(f)
            if r=="C": best_rank="C"; break
            if r.startswith("#"):
                n=int(r[1:])
                if best_rank=="NR" or n < int(best_rank[1:] if best_rank.startswith("#") else 999):
                    best_rank=r
        save_line=f"Save:  Wk {gw}, {gy}  |  Funds: {gf}  |  Fighters: {gfighters}  |  Best Rank: {best_rank}"
        print(f"{CY}║{RST}{_pc(f'{CG}{save_line}{RST}',TW-2)}{CY}║{RST}")
        print(f"{CY}║{RST}{' '*(TW-2)}{CY}║{RST}")
        opts_line = f"{DIM}[{RST}{CW}N{RST}{DIM}]{RST} {CY}New Game{RST}   {DIM}[{RST}{CW}L{RST}{DIM}]{RST} {CY}Load Save{RST}   {DIM}[{RST}{CW}X{RST}{DIM}]{RST} {CY}Exit{RST}"
    else:
        print(f"{CY}║{RST}{_pc(f'{DIM}No save file found — start a new career below.{RST}',TW-2)}{CY}║{RST}")
        print(f"{CY}║{RST}{' '*(TW-2)}{CY}║{RST}")
        opts_line = f"{DIM}[{RST}{CW}N{RST}{DIM}]{RST} {CY}New Game{RST}   {DIM}[{RST}{CW}X{RST}{DIM}]{RST} {CY}Exit{RST}"

    print(f"{CY}║{RST}{_pc(opts_line,TW-2)}{CY}║{RST}")
    print(f"{CY}║{RST}{' '*(TW-2)}{CY}║{RST}")
    print(f"{CY}╚{'═'*(TW-2)}╝{RST}\n")

    while True:
        c = input(f"{CY}>{RST} ").strip().upper()
        if c == 'N':
            return None
        elif c == 'L' and existing:
            print(f"\n  {CG}Save loaded! Week {existing.week}, {existing.year}{RST}")
            time.sleep(1)
            return existing
        elif c == 'X':
            sys.exit()

def menu_create_fighter(game):
    """Character creation screen at game start."""
    clear_screen()
    print(f"{CY}\u2554{'═'*(TW-2)}\u2557{RST}")
    print(f"{CY}\u2551{RST}{_pc(f'{BLD}{CW} CREATE YOUR FIGHTER {RST}',TW-2)}{CY}\u2551{RST}")
    print(f"{CY}\u2560{'═'*(TW-2)}\u2563{RST}")
    print(f"{CY}\u2551{RST}  {DIM}Build your fighter from the ground up. Choose wisely.{RST}{' '*(TW-56)}{CY}\u2551{RST}")
    print(f"{CY}\u255a{'═'*(TW-2)}\u255d{RST}\n")

    name=input(f"  {CY}Fighter Name{RST} (press Enter for default): ").strip()
    if not name: name="The Protagonist"

    nick_in=input(f"  {CY}Nickname{RST} (optional, press Enter to skip): ").strip()
    nickname=nick_in if nick_in else None

    print(f"\n  {CY}── WEIGHT CLASS ──{RST}")
    for i,wc in enumerate(MEN_WEIGHT_CLASSES):
        print(f"  {DIM}[{RST}{CW}{i+1}{RST}{DIM}]{RST}  {wc}")
    try:    weight_class=MEN_WEIGHT_CLASSES[int(input(f"\n  {CY}>{RST} "))-1]
    except: weight_class="Lightweight (155 lbs)"

    print(f"\n  {CY}── FIGHTING STYLE ──{RST}")
    style_opts=[
        ("1","Striker",  "High striking,  lower grappling.  Danger on the feet."),
        ("2","Grappler", "High grappling, lower striking.   Dominant on the mat."),
        ("3","Brawler",  "High power,     lower technique.  Tough as nails."),
        ("4","Balanced", "Even all-round stats.             Comfortable everywhere."),
    ]
    for k,s,desc in style_opts:
        print(f"  {DIM}[{RST}{CW}{k}{RST}{DIM}]{RST} {CY}{s:<12}{RST} {DIM}{desc}{RST}")
    sm={"1":"Striker","2":"Grappler","3":"Brawler","4":"Balanced"}
    style=sm.get(input(f"\n  {CY}>{RST} ").strip(),"Balanced")

    print(f"\n  {CY}── MENTALITY ──{RST}")
    pers_opts=[
        ("1","Aggressive","Always looking for the finish. High-pressure style."),
        ("2","Technical",  "Disciplined and precise. High striking accuracy."),
        ("3","Explosive",  "Fast starter and finisher. Loses steam in later rounds."),
        ("4","Calculated", "Patient and cerebral. Gets stronger in championship rounds."),
        ("5","Wild",       "Unpredictable chaos — high variance, high entertainment."),
        ("6","Composed",   "Ice cold under pressure. Performs best when hurt."),
    ]
    for k,p,desc in pers_opts:
        print(f"  {DIM}[{RST}{CW}{k}{RST}{DIM}]{RST} {CY}{p:<12}{RST} {DIM}{desc}{RST}")
    pm={"1":"Aggressive","2":"Technical","3":"Explosive","4":"Calculated","5":"Wild","6":"Composed"}
    personality=pm.get(input(f"\n  {CY}>{RST} ").strip(),"Technical")

    f=Fighter(name,22,style,weight_class,is_player=True)
    f.nickname=nickname; f.personality=personality
    if style=="Striker":
        f.striking=72;f.grappling=52;f.defense=66;f.strength=62;f.toughness=65
    elif style=="Grappler":
        f.striking=52;f.grappling=74;f.defense=60;f.strength=65;f.toughness=65
    elif style=="Brawler":
        f.striking=66;f.grappling=56;f.defense=52;f.strength=74;f.toughness=76
    else:
        f.striking=65;f.grappling=65;f.defense=62;f.strength=62;f.toughness=64

    print(f"\n  {CG}Fighter created: {CW}{f.display_name}{RST}  {DIM}| {style} | {personality} | {weight_class}{RST}")
    input(f"  {DIM}Press ENTER to begin your career...{RST}")
    return f

def menu_fighter_view(game, fighter, editable=False):
    """View detailed profile of any fighter (world or gym)."""
    while True:
        draw_header(fighter.display_name, game)
        rank=game.get_fighter_rank(fighter)
        rec=f"{fighter.record['W']}-{fighter.record['L']}-{fighter.record['D']}"

        nick_s=f'  {CY}"{fighter.nickname}"{RST}' if fighter.nickname else ""
        print(f"  {CW}{BLD}{fighter.name}{RST}{nick_s}")
        print(f"  {DIM}Age {fighter.age}  |  {fighter.weight_class}  |  {fighter.style}  |  {fighter.personality}{RST}")
        print(f"  Rank: {CY}{rank}{RST}   Record: {CG}{rec}{RST}   Streak: {fighter.streak_str}   KOs: {CW}{fighter.career_kos}{RST}")
        print(f"  Fame: {fame_bar(fighter.fame)}   Peak: {CY}{'C' if fighter.peak_rank==0 else ('#'+str(fighter.peak_rank) if fighter.peak_rank<=15 else 'NR')}{RST}")

        print(f"\n  {CY}ATTRIBUTES{RST}")
        print(f"  {DIM}{'─'*(TW-4)}{RST}")
        stats=[("STRIKING",fighter.striking),("GRAPPLING",fighter.grappling),
               ("DEFENSE",fighter.defense),("STAMINA",fighter.stamina),
               ("STRENGTH",fighter.strength),("TOUGHNESS",fighter.toughness)]
        for i in range(0,len(stats),2):
            n1,v1=stats[i]
            left=f"  {DIM}{n1:<10}{RST} {draw_bar(v1,100,12)}"
            if i+1<len(stats):
                n2,v2=stats[i+1]
                right=f"  {DIM}{n2:<10}{RST} {draw_bar(v2,100,12)}"
                print(f"{_pr(left,40)}{right}")
            else: print(left)

        if fighter.achievements:
            print(f"\n  {CY}ACHIEVEMENTS{RST}")
            print(f"  {DIM}{'─'*(TW-4)}{RST}")
            for ach in fighter.achievements:
                print(f"  {CM}\u2605{RST}  {ach}")

        if fighter.fight_history:
            print(f"\n  {CY}RECENT RESULTS{RST}")
            print(f"  {DIM}{'─'*(TW-4)}{RST}")
            print(f"  {DIM}{'Res':<5}{'Opponent':<22}{'Method':<14}{'Rnd':<5}Date{RST}")
            for fh in reversed(fighter.fight_history[-8:]):
                col=CG if fh["result"]=="W" else CR if fh["result"]=="L" else CY
                print(f"  {col}{fh['result']:<5}{RST}{fh['opponent'][:20]:<22}"
                      f"{DIM}{fh['method']:<14}R{fh['round']:<4}Wk{fh['week']},{fh['year']}{RST}")
        else:
            print(f"\n  {DIM}No fight history on record.{RST}")

        print(f"\n{CY}{'═'*TW}{RST}")
        if editable:
            sf=game.scheduled_fight
            in_camp=sf and sf["fighter"]==fighter
            if in_camp:
                print(f"  {DIM}[{RST}{CW}C{RST}{DIM}]{RST} Camp Training  "
                      f"{DIM}[{RST}{CW}F{RST}{DIM}]{RST} View Opponent  "
                      f"{DIM}[{RST}{CW}B{RST}{DIM}]{RST} Back")
            else:
                print(f"  {DIM}[{RST}{CW}F{RST}{DIM}]{RST} Book a Fight  "
                      f"{DIM}[{RST}{CW}B{RST}{DIM}]{RST} Back")
            c=input(f"\n  {CY}>{RST} ").lower()
            if c=='b': return
            elif c=='c' and in_camp: menu_camp(game)
            elif c=='f':
                if in_camp:
                    opp=sf["opponent"]
                    print(f"\n  {CY}OPPONENT: {opp.display_name}{RST}")
                    print(f"  {DIM}STR:{CW}{opp.striking}{DIM} GRP:{CW}{opp.grappling}{DIM} "
                          f"DEF:{CW}{opp.defense}{DIM} STA:{CW}{opp.stamina}{RST}")
                    input(f"  {DIM}Press ENTER...{RST}")
                elif not game.scheduled_fight:
                    menu_matchmaking(game,fighter)
                    return
        else:
            input(f"  {DIM}Press ENTER to go back...{RST}")
            return

def menu_main(game):
    LW,RW=20,55
    while True:
        clear_screen(); sf=game.scheduled_fight
        print(f"{CY}\u2554{'═'*(TW-2)}\u2557{RST}")
        title=f"{BLD}{CY} \u2605 {CW}MMA LEGENDS{CY} \u2605{RST}"
        funds=f"{CG}${game.funds:,}{RST}"
        date=f"{DIM}WEEK {game.week}, {game.year} {RST}"
        pad=TW-2-_vis(title)-_vis(funds)-2-len(f"WEEK {game.week}, {game.year} ")
        print(f"{CY}\u2551{RST}{title}  {funds}{' '*max(1,pad)}{date}{CY}\u2551{RST}")
        if sf:
            wl=sf["weeks_total"]-sf["weeks_done"]
            cs=f"{CM} CAMP: {sf['fighter'].name} vs {sf['opponent'].name[:14]}  [{sf['fight_type'].upper()}]  {wl}wk left {RST}"
            print(f"{CY}\u2551{RST}{_pc(cs,TW-2)}{CY}\u2551{RST}")
        print(f"{CY}\u2560{'═'*LW}\u2566{'═'*RW}\u2563{RST}")

        opts=[("1","MY GYM"),("2","RANKINGS"),("3","RECORDS"),("4","RECRUIT")]
        if sf: opts.append(("C","CAMP TRAIN"))
        opts+=[("5","ADVANCE WEEK"),("S","SAVE GAME"),("7","CHEATS"),("6","EXIT")]

        news_lines=[]
        for item in (game.news_feed if game.news_feed else ["Quiet week."]):
            col=_news_color(item)
            for seg in _wrap(item,RW-3):
                news_lines.append((col,seg))

        print(f"{CY}\u2551{RST}{_pr(f'  {CY}MENU{RST}',LW)}{CY}\u2551{RST}{_pr(f'  {CY}NEWS & EVENTS{RST}',RW)}{CY}\u2551{RST}")
        sl=_pr(f"  {DIM}{'─'*(LW-4)}{RST}",LW); sr=_pr(f"  {DIM}{'─'*(RW-4)}{RST}",RW)
        print(f"{CY}\u2551{RST}{sl}{CY}\u2551{RST}{sr}{CY}\u2551{RST}")
        n_rows=max(len(opts),len(news_lines))
        for i in range(n_rows):
            if i<len(opts):
                k,lbl=opts[i]
                btn=f"  {DIM}[{RST}{CW}{k}{RST}{DIM}]{RST} {CY}{lbl}{RST}"
                lc=_pr(btn,LW)
            else: lc=' '*LW
            if i<len(news_lines):
                col,nl=news_lines[i]
                rc=_pr(f"  {col}{nl}{RST}",RW)
            else:
                rc=' '*RW
            print(f"{CY}\u2551{RST}{lc}{CY}\u2551{RST}{rc}{CY}\u2551{RST}")
        print(f"{CY}\u255a{'═'*LW}\u2569{'═'*RW}\u255d{RST}")

        c=input(f"\n{CY}>{RST} ").strip().upper()
        if   c=='1': menu_gym(game)
        elif c=='2': menu_rankings(game)
        elif c=='3': menu_records(game)
        elif c=='4': menu_recruit(game)
        elif c=='C' and sf: menu_camp(game)
        elif c=='5':
            result=game.advance_week()
            if result=="FIGHT_TIME":
                sf2=game.scheduled_fight
                print(f"\n  {CM}{BLD}FIGHT CAMP COMPLETE!{RST}")
                print(f"  {CW}{sf2['fighter'].name}{RST} vs {CW}{sf2['opponent'].name}{RST}")
                input(f"  {DIM}Press ENTER to start the fight...{RST}")
                FightManager(sf2["fighter"],sf2["opponent"],game,sf2["fight_type"]).run()
            else:
                print(f"  {CC}World results simulated...{RST}"); time.sleep(0.6)
        elif c=='S':
            if save_game(game):
                print(f"  {CG}Game saved! Week {game.week}, {game.year}  Funds: ${game.funds:,}{RST}")
            else:
                print(f"  {CR}Save failed!{RST}")
            time.sleep(1.2)
        elif c=='7': menu_cheats(game)
        elif c=='6':
            c2=input(f"  {DIM}Save before exit? [Y/N]: {RST}").strip().upper()
            if c2=='Y': save_game(game)
            sys.exit()

def menu_camp(game):
    sf=game.scheduled_fight
    if not sf: return
    fighter=sf["fighter"]
    while True:
        draw_header(f"FIGHT CAMP — {sf['fight_type'].upper()}",game)
        wdone=sf["weeks_done"]; wtotal=sf["weeks_total"]
        bar_len=30; filled=int(bar_len*wdone/wtotal) if wtotal else 0
        bar=f"{CG}{'█'*filled}{DIM}{'░'*(bar_len-filled)}{RST}"
        print(f"  {CY}Camp Progress:{RST} {bar} {CW}{wdone}/{wtotal}wk{RST}  Remaining: {CY}{wtotal-wdone}{RST}")
        print(f"  {DIM}Opponent:{RST} {CW}{sf['opponent'].name}{RST}  "
              f"Rank: {CY}{game.get_fighter_rank(sf['opponent'])}{RST}  "
              f"Style: {DIM}{sf['opponent'].style}{RST}  "
              f"Fame: {CM}{sf['opponent'].fame}/100{RST}")

        # Show opponent weaknesses
        opp=sf["opponent"]
        weak=min(("striking",opp.striking),("grappling",opp.grappling),
                 ("defense",opp.defense),key=lambda x:x[1])
        print(f"  {DIM}Scout:{RST} {CY}Exploit {weak[0]} ({weak[1]}){RST}  "
              f"Str:{opp.striking}  Grp:{opp.grappling}  Def:{opp.defense}")

        print(f"  {DIM}{'─'*(TW-4)}{RST}")
        print(f"  {CW}{BLD}{fighter.name}{RST}  Fame: {CM}{fighter.fame}/100{RST}  "
              f"Camp Stamina: {CY}{fighter.weekly_stamina}{RST}/100  "
              f"Funds: {CG}${game.funds:,}{RST}")
        stats_l=(f"  STR:{CW}{fighter.striking:>2}{RST} "
                 f"GRP:{CW}{fighter.grappling:>2}{RST} "
                 f"DEF:{CW}{fighter.defense:>2}{RST} "
                 f"STA:{CW}{fighter.stamina:>2}{RST} "
                 f"PWR:{CW}{fighter.strength:>2}{RST} "
                 f"TGH:{CW}{fighter.toughness:>2}{RST}")
        print(stats_l)
        print(f"  {DIM}{'─'*(TW-4)}{RST}")
        print(f"  {CY}TRAINING DRILLS{RST}")
        for k,label,cost,stam,stat,lo,hi,desc in CAMP_DRILLS:
            cs=f"{CG}${cost:,}{RST}" if cost else f"{DIM}Free  {RST}"
            ss=(f"{CG}+{-stam} sta{RST}" if stam<0 else f"{CR}-{stam} sta{RST}")
            gs=(f"{CC}all+1{RST}" if stat=="all" else f"{CG}recover{RST}" if stat=="rest" else f"{CC}+{lo}-{hi}{RST}")
            print(f"  {DIM}[{RST}{CW}{k}{RST}{DIM}]{RST} {label:<22} {cs:<14} {ss}  {gs}  {DIM}{desc}{RST}")
        print(f"  {DIM}{'─'*(TW-4)}{RST}")
        print(f"  {DIM}[{RST}{CW}B{RST}{DIM}]{RST} Done for this week")
        c=input(f"\n{CY}>{RST} ").strip().upper()
        if c=='B': return
        ok,msg=fighter.do_drill(c,game)
        print(msg); time.sleep(0.7)

def menu_records(game):
    """Records screen with legendary targets and progress bars."""
    while True:
        draw_header("RECORDS & LEGENDS", game)

        print(f"  {CY}WORLD RECORDS{RST}  {DIM}— Chase the legends. Break the marks. Write history.{RST}")
        print(f"  {DIM}{'─'*(TW-4)}{RST}")

        for rec_name, rv in game.records.items():
            cur_val    = rv['val']
            tgt_val    = rv.get('target_val', 0)
            tgt_holder = rv.get('target_holder', 'Unknown')
            lower_b    = rv.get('lower_better', False)
            is_cur     = rv.get('currency', False)
            sfx        = rv.get('sfx', '')

            def _fmt(v):
                if is_cur: return f"${v:,}"
                return f"{v}{sfx}"

            unset = (lower_b and cur_val == 999) or (not lower_b and cur_val == 0)
            if unset:
                pct = 0.0
            elif lower_b:
                pct = min(1.0, tgt_val / cur_val) if cur_val > 0 else 1.0
            else:
                pct = min(1.0, cur_val / tgt_val) if tgt_val > 0 else 1.0

            beaten = (lower_b and not unset and cur_val <= tgt_val) or \
                     (not lower_b and cur_val >= tgt_val)

            bar = draw_prog_bar(pct, length=16, broken=beaten)

            if beaten:
                pct_str = f"{CG}BROKEN!{RST}"
                name_col = CG
            elif unset:
                pct_str = f"{DIM}  0%{RST}"
                name_col = DIM
            else:
                pct_str = f"{CW}{int(pct*100):>3}%{RST}"
                name_col = CW

            if unset:
                cur_str = f"{DIM}Not Set{RST}"
            else:
                h_short = rv['holder'][:18]
                cur_str = f"{CC}{_fmt(cur_val)}{RST} {DIM}{h_short}{RST}"

            tgt_str = _fmt(tgt_val)

            # Line 1: name + bar + pct + current holder
            print(f"  {name_col}{rec_name:<24}{RST}  {bar} {pct_str:<12}  {cur_str}")
            # Line 2: target to beat
            print(f"  {DIM}{'':>24}  └─ Legend to beat: {CY}{tgt_str}{DIM} — {tgt_holder[:32]}{RST}")

        # Hall of Fame
        print(f"\n  {CY}HALL OF FAME{RST}")
        print(f"  {DIM}{'─'*(TW-4)}{RST}")
        for leg in game.hall_of_fame:
            print(f"  {CY}\u2605{RST}  {CW}{leg['name']:<24}{RST}  {DIM}{leg['reason']}{RST}")

        # Manager stats
        print(f"\n  {DIM}{'─'*(TW-4)}{RST}")
        print(f"  {DIM}Total manager income:{RST}  {CG}${game.total_income:,}{RST}  "
              f"{DIM}Win bonuses earned:{RST}  {CY}{game.total_bonuses}{RST}")
        mgr_pct = min(1.0, game.total_income / 12_000_000)
        print(f"  {DIM}Dynasty progress:{RST}  {draw_prog_bar(mgr_pct,length=24)}  {CW}{int(mgr_pct*100)}%{RST}")

        print(f"\n{CY}{'═'*TW}{RST}")
        input(f"  {DIM}Press ENTER to go back...{RST}")
        return

def menu_rankings(game):
    while True:
        draw_header("GLOBAL RANKINGS",game)
        for i,wc in enumerate(MEN_WEIGHT_CLASSES):
            print(f"  {DIM}[{RST}{CW}{i+1}{RST}{DIM}]{RST}  {wc}")
        c=input(f"\n{CY}>{RST} Select class (or 'b'): ")
        if c=='b': return
        try:
            wc=MEN_WEIGHT_CLASSES[int(c)-1]
            roster=game.world_roster[wc]
            while True:
                draw_header(f"{wc} Rankings",game)
                champ=roster[0]
                crec=f"{CG}{champ.record['W']}{DIM}-{CR}{champ.record['L']}{RST}"
                cn=f' {CY}"{champ.nickname}"{RST}' if champ.nickname else ""
                print(f"  {CY}{BLD}CHAMPION{RST}  {CW}{BLD}{champ.name}{RST}{cn}  "
                      f"{DIM}({RST}{crec}{DIM})  Fame:{CM}{champ.fame}{RST}  "
                      f"Str:{champ.streak_str}  {DIM}{champ.style}{RST}")
                print(f"  {DIM}{'─'*(TW-4)}{RST}")
                print(f"  {DIM}{'#':<5}{'Name':<20}{'Record':<10}{'Streak':<9}{'Fame':<6}Style{RST}")
                print(f"  {DIM}{'─'*(TW-4)}{RST}")
                for i in range(1,16):
                    if i>=len(roster): break
                    f=roster[i]
                    col=CG if i<=5 else CW
                    rec=f"{CG}{f.record['W']}{RST}{DIM}-{RST}{CR}{f.record['L']}{RST}"
                    nick=f' {DIM}"{f.nickname[:10]}"{RST}' if f.nickname else ""
                    sk=(f"{CG}W{f.win_streak}{RST}" if f.win_streak>=2
                        else f"{CR}L{f.loss_streak}{RST}" if f.loss_streak>=2 else f"{DIM}—{RST}")
                    print(f"  {col}#{i:<4}{RST}{f.name[:16]:<16}{nick[:12]:<12}"
                          f"  {rec:<12}  {sk:<10}  {CM}{f.fame:>3}{RST}  {DIM}{f.style}{RST}")
                print(f"\n  {CY}{'─'*(TW-4)}{RST}")
                print(f"  {DIM}Enter # to view profile | [0] Champion | [b] back{RST}")
                sel=input(f"\n{CY}>{RST} ").strip()
                if sel=='b': break
                try:
                    idx=int(sel)
                    if idx==0: menu_fighter_view(game,roster[0])
                    elif 1<=idx<=15 and idx<len(roster): menu_fighter_view(game,roster[idx])
                except: pass
        except: pass

def menu_gym(game):
    while True:
        draw_header("YOUR GYM",game); sf=game.scheduled_fight
        if sf:
            fi=sf["fighter"]; wl=sf["weeks_total"]-sf["weeks_done"]
            print(f"  {CM}Active Camp:{RST} {CW}{fi.name}{RST} vs {CW}{sf['opponent'].name}{RST}  "
                  f"{CY}{wl} week(s) until fight{RST}")
            print(f"  {DIM}{'─'*(TW-4)}{RST}")
        if not game.gym_roster:
            print(f"  {DIM}No fighters signed. Visit Recruitment.{RST}")
            input(f"  {DIM}Press ENTER...{RST}"); return
        print(f"  {DIM}{'#':<3}{'Name':<20}{'Rank':<5}{'Record':<10}{'Fame':<7}Stamina{RST}")
        print(f"  {DIM}{'─'*62}{RST}")
        for i,f in enumerate(game.gym_roster):
            rank=game.get_fighter_rank(f)
            rec=f"{CG}{f.record['W']}{RST}{DIM}-{RST}{CR}{f.record['L']}{RST}"
            stam=draw_bar(f.weekly_stamina,100,8)
            camp_flag=f"  {CM}*CAMP*{RST}" if(sf and sf["fighter"]==f) else ""
            print(f"  {DIM}[{RST}{CW}{i+1}{RST}{DIM}]{RST} {f.name:<20} {CY}{rank:<5}{RST} "
                  f"{rec:<10}  {CM}{f.fame:>3}{RST}   {stam}{camp_flag}")

        # Gym overview stats
        if game.gym_roster:
            tw,tl,tkos,best = game.gym_stats()
            print(f"  {DIM}{'─'*(TW-4)}{RST}")
            print(f"  {DIM}Gym Record:{RST}  {CG}{tw}W{RST} {DIM}/{RST} {CR}{tl}L{RST}   "
                  f"{DIM}Total KOs:{RST} {CW}{tkos}{RST}   "
                  f"{DIM}Total Earned:{RST} {CG}${game.total_income:,}{RST}")
            if best:
                print(f"  {DIM}Star Fighter:{RST}  {CW}{best.name}{RST}  "
                      f"Fame: {CM}{best.fame}/100{RST}  Rank: {CY}{game.get_fighter_rank(best)}{RST}")

        c=input(f"\n{CY}>{RST} Select fighter (or 'b'): ")
        if c=='b': return
        try: menu_fighter_view(game,game.gym_roster[int(c)-1],editable=True)
        except: pass

def menu_matchmaking(game,fighter):
    roster=game.world_roster[fighter.weight_class]
    my_idx=game.get_rank_index(fighter)
    if my_idx==999: my_idx=len(roster)-1
    start=max(0,my_idx-5); end=min(len(roster),my_idx+8)
    draw_header("MATCHMAKING",game)
    print(f"  Book fight for: {CW}{BLD}{fighter.name}{RST}  {DIM}({fighter.weight_class}){RST}\n")
    print(f"  {DIM}Unranked=4wk  Ranked=6-8wk  Contender=6-8wk  Championship=8-10wk{RST}")
    print(f"  {DIM}{'#':<5}{'Name':<22}{'Record':<10}{'Str':<8}{'STR':<5}{'GRP':<5}Type{RST}")
    print(f"  {DIM}{'─'*62}{RST}")
    opps,count=[],1
    for i in range(start,end):
        opp=roster[i]
        if opp==fighter: continue
        rank=game.get_fighter_rank(opp)
        rec=f"{opp.record['W']}-{opp.record['L']}"
        ft=game.get_fight_type(opp)
        fc={("championship",CM),("contender",CR),("ranked",CY),("unranked",CG)}
        fc=dict(fc).get(ft,CW)
        sk=(f"W{opp.win_streak}" if opp.win_streak>=2 else f"L{opp.loss_streak}" if opp.loss_streak>=2 else "—")
        rc=CY if i==0 else CG if i<=5 else CW
        print(f"  {DIM}[{RST}{CW}{count}{RST}{DIM}]{RST} {rc}{rank:<4}{RST} {opp.name[:20]:<22} "
              f"{DIM}{rec:<10}{sk:<8}{opp.striking:<5}{opp.grappling:<5}{RST}{fc}{ft.upper()}{RST}")
        opps.append(opp); count+=1
    c=input(f"\n{CY}>{RST} Select opponent (or 'b'): ").strip()
    if c=='b': return
    try:
        opp=opps[int(c)-1]
        ft,wks=game.book_fight(fighter,opp)
        print(f"\n  {CG}Fight booked! {ft.upper()} — {wks}-week camp starts now.{RST}")
        print(f"  {DIM}Use [C] CAMP TRAIN from main menu to train each week.{RST}")
        time.sleep(2)
    except: pass

def menu_cheats(game):
    """Cheat menu — full list of cheats with fighter selection where needed."""
    CHEATS = [
        ("1",  "Add $500,000",           "Inject $500K into manager funds"),
        ("2",  "Add $2,000,000",         "Inject $2M into manager funds"),
        ("3",  "Add $10,000,000",        "Set funds to $10,000,000 + current"),
        ("4",  "Max Fighter Stats",      "Set all stats to 99 for one fighter"),
        ("5",  "Max Fighter Fame",       "Set fame to 100 for one fighter"),
        ("6",  "Add 10 Wins",            "Add 10 wins + fame to a fighter's record"),
        ("7",  "Add 5-Win Streak",       "Give a fighter a 5-fight winning streak"),
        ("8",  "Instant Champion",       "Move a fighter to #1 in their division"),
        ("9",  "Skip Camp",              "Instantly complete the current fight camp"),
        ("G",  "Toggle God Mode",        "Your fighters take zero damage in fights"),
        ("K",  "Add $1M & Max All Gym",  "Mega boost: cash + max stats for all gym fighters"),
        ("R",  "Reset Save",             "Delete the save file (irreversible!)"),
        ("B",  "Back",                   "Return to main menu"),
    ]

    def _pick_gym_fighter(prompt="Select fighter: "):
        if not game.gym_roster:
            print(f"  {CR}No fighters in gym.{RST}"); time.sleep(1); return None
        for i,f in enumerate(game.gym_roster):
            gm_flag = f"  {CM}[GOD]{RST}" if getattr(f,'god_mode',False) else ""
            print(f"  {DIM}[{RST}{CW}{i+1}{RST}{DIM}]{RST}  {f.name:<22} {DIM}{f.style}{RST}{gm_flag}")
        try:    return game.gym_roster[int(input(f"  {CY}>{RST} {prompt}"))-1]
        except: return None

    while True:
        draw_header("CHEAT CODES", game)

        # Show god mode status for all gym fighters
        gm_fighters = [f for f in game.gym_roster if getattr(f,'god_mode',False)]
        if gm_fighters:
            print(f"  {CM}{BLD}GOD MODE ACTIVE:{RST}  {', '.join(f.name for f in gm_fighters)}")
        else:
            print(f"  {DIM}God Mode: OFF{RST}")

        print(f"  {DIM}{'─'*(TW-4)}{RST}")
        print(f"  {CW}Funds:{RST} {CG}${game.funds:,}{RST}   "
              f"{CW}Week:{RST} {DIM}{game.week}, {game.year}{RST}   "
              f"{CW}Fighters:{RST} {DIM}{len(game.gym_roster)}{RST}")
        print(f"  {DIM}{'─'*(TW-4)}{RST}")

        for k, label, desc in CHEATS:
            col = CR if k in ("R","B") else CM if k=="G" else CY
            print(f"  {DIM}[{RST}{CW}{k}{RST}{DIM}]{RST}  {col}{label:<28}{RST}  {DIM}{desc}{RST}")

        print(f"\n{CY}{'═'*TW}{RST}")
        c = input(f"\n{CY}>{RST} ").strip().upper()

        if c == 'B':
            return

        elif c == '1':
            game.funds += 500_000
            print(f"  {CG}+$500,000 added. Funds: ${game.funds:,}{RST}")

        elif c == '2':
            game.funds += 2_000_000
            print(f"  {CG}+$2,000,000 added. Funds: ${game.funds:,}{RST}")

        elif c == '3':
            game.funds += 10_000_000
            print(f"  {CG}+$10,000,000 added. Funds: ${game.funds:,}{RST}")

        elif c == '4':
            print(f"\n  {CY}── MAX STATS — SELECT FIGHTER ──{RST}")
            f = _pick_gym_fighter()
            if f:
                for stat in ("striking","grappling","defense","stamina","strength","toughness"):
                    setattr(f, stat, 99)
                print(f"  {CG}All stats set to 99 for {f.name}.{RST}")

        elif c == '5':
            print(f"\n  {CY}── MAX FAME — SELECT FIGHTER ──{RST}")
            f = _pick_gym_fighter()
            if f:
                f.fame = 100
                print(f"  {CG}Fame set to 100 for {f.name}.{RST}")

        elif c == '6':
            print(f"\n  {CY}── ADD 10 WINS — SELECT FIGHTER ──{RST}")
            f = _pick_gym_fighter()
            if f:
                for _ in range(10): f.add_win(by_finish=random.random()<0.4)
                print(f"  {CG}+10 wins added to {f.name}. Record: {f.record['W']}-{f.record['L']}{RST}")

        elif c == '7':
            print(f"\n  {CY}── ADD WIN STREAK — SELECT FIGHTER ──{RST}")
            f = _pick_gym_fighter()
            if f:
                f.win_streak = max(f.win_streak, 5)
                print(f"  {CG}Win streak set to {f.win_streak} for {f.name}.{RST}")

        elif c == '8':
            print(f"\n  {CY}── INSTANT CHAMPION — SELECT FIGHTER ──{RST}")
            f = _pick_gym_fighter()
            if f:
                roster = game.world_roster.get(f.weight_class, [])
                if f in roster: roster.remove(f)
                roster.insert(0, f)
                f.peak_rank = 0; f.fame = min(100, f.fame+20)
                game.check_player_achievements(f)
                print(f"  {CG}{f.name} is now CHAMPION of {f.weight_class}!{RST}")

        elif c == '9':
            sf = game.scheduled_fight
            if sf:
                sf["weeks_done"] = sf["weeks_total"]
                print(f"  {CG}Camp instantly completed. Advance a week to trigger the fight.{RST}")
            else:
                print(f"  {CR}No fight camp currently scheduled.{RST}")

        elif c == 'G':
            print(f"\n  {CY}── TOGGLE GOD MODE — SELECT FIGHTER ──{RST}")
            f = _pick_gym_fighter()
            if f:
                f.god_mode = not getattr(f,'god_mode',False)
                state = f"{CG}ON{RST}" if f.god_mode else f"{CR}OFF{RST}"
                print(f"  God Mode {state} for {CW}{f.name}{RST}.")

        elif c == 'K':
            game.funds += 1_000_000
            for f in game.gym_roster:
                for stat in ("striking","grappling","defense","stamina","strength","toughness"):
                    setattr(f, stat, 99)
                f.fame = 100
            print(f"  {CG}MEGA BOOST! +$1M and all gym fighters maxed.{RST}")

        elif c == 'R':
            confirm = input(f"  {CR}Delete save file? Type 'YES' to confirm: {RST}").strip()
            if confirm == 'YES':
                delete_save()
                print(f"  {CG}Save file deleted.{RST}")
            else:
                print(f"  {DIM}Cancelled.{RST}")

        time.sleep(0.9)

def menu_recruit(game):
    draw_header("SCOUTING",game)
    recruits=[]
    for _ in range(3):
        wc=random.choice(MEN_WEIGHT_CLASSES)
        f=Fighter(generate_name(),random.randint(19,23),random.choice(Fighter.STYLES),wc,cost=5000)
        recruits.append(f)
    print(f"  {DIM}{'#':<4}{'Name':<22}{'Weight Class':<26}{'Style':<12}Cost{RST}")
    print(f"  {DIM}{'─'*66}{RST}")
    for i,r in enumerate(recruits):
        print(f"  {DIM}[{RST}{CW}{i+1}{RST}{DIM}]{RST}  {r.name:<22} "
              f"{DIM}{r.weight_class:<26}{r.style:<12}{RST}{CY}${r.contract_value:,}{RST}")
    c=input(f"\n{CY}>{RST} Sign recruit #: ")
    try:
        r=recruits[int(c)-1]
        if game.funds>=r.contract_value:
            game.funds-=r.contract_value; r.is_player=True
            game.gym_roster.append(r)
            game.world_roster[r.weight_class].append(r)
            print(f"  {CG}Signed {r.name}! ({r.style}){RST}"); time.sleep(1)
        else:
            print(f"  {CR}Insufficient funds.{RST}"); time.sleep(1)
    except: pass

# ─── ENTRY POINT ────────────────────────────────────────────────────────────────
if __name__=="__main__":
    loaded = menu_title_screen()
    if loaded:
        g = loaded
    else:
        g = GameState()
        starter = menu_create_fighter(g)
        g.gym_roster.append(starter)
        g.world_roster[starter.weight_class].insert(40, starter)
    menu_main(g)

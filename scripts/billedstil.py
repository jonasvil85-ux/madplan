"""Billedstil og faglige beskrivelser til AI-billederne (bruges af billeder.py).

Billedmodellen kender ikke danske retter, så hver ret får:
  1. en kort, FAGLIG beskrivelse af hvordan netop den ret ser ud (DETALJER: fx hvordan stegt flæsk, medister og frikadeller ser ud),
  2. en køkkenstil (STIL_KOEKKEN): dansk ser dansk ud, italiensk ser italiensk ud osv. – alt sammen i en moderne nordisk fotostil.
Tilføj nye retter øverst i DETALJER (første match vinder). Retter uden match får deres håndskrevne beskrivelse fra billedprompts.json."""
import re

# Fælles nordisk gastronomisk fotostil (New Nordic): blødt dagslys, lyst træ, hør, enkelt hvidt porcelæn, reduceret anretning
STIL_NORDISK = ('Editorial cookbook food photograph in a modern Nordic style: soft natural window daylight, light oak table, muted linen cloth, '
                'simple matte white porcelain, restrained honest plating, shallow depth of field, shot from a 45 degree angle, '
                'realistic, appetizing, freshly cooked, no text, no people, no hands')

STIL_KOEKKEN = {
    'dansk': 'Traditional Danish home cooking (dansk husmandskost) on a plain white porcelain plate, generous honest portion, with fresh green parsley',
    'italiensk': 'Authentic Italian dish: fresh basil, freshly grated parmesan, glossy olive oil, rustic stoneware bowl or plate',
    'amerikansk': 'American comfort food, generous and casual, served on a wooden board or simple plate',
    'asiatisk': 'Asian home-style dish served in a bowl with chopsticks, garnished with spring onion and sesame seeds',
    'middelhav': 'Mediterranean dish with olive oil, lemon, fresh herbs and feta, served on a stoneware plate',
    'vegetar': 'Colourful vegetarian dish with fresh vegetables and herbs',
}

# (regex på rettens navn i små bogstaver, beskrivelse af hvordan retten SER UD) – første match vinder
DETALJER = [
    (r'stegt flæsk', 'Danish stegt flæsk med persillesovs: several thick slices of crispy golden-brown fried pork belly with crunchy edges, beside a mound of boiled potatoes, '
                     'covered in a creamy pale-green parsley sauce with flecks of chopped fresh parsley'),
    (r'æbleflæsk', 'Danish æbleflæsk: slices of fried pork belly with soft caramelised apple and onion, served on dark rye bread'),
    (r'medister', 'Danish medisterpølse: thick coarse-ground pork sausage fried until the casing is glossy golden-brown, sliced diagonally to show the pale pink coarse meat inside'),
    (r'frikadeller|grisefrikadel', 'Danish frikadeller: several flat oval pan-fried meatballs of minced pork and veal with a golden-brown uneven crust'),
    (r'fiskefrikadeller', 'Danish fiskefrikadeller: flat oval pan-fried fish cakes with a golden crust, with remoulade, a lemon wedge and boiled potatoes'),
    (r'flæskesteg|ribbensteg', 'Danish flæskesteg: slices of roast pork with golden bubbly crackling (svær) on top, juicy pale pink meat, with caramelised brown potatoes and red cabbage'),
    (r'forloren hare', 'Danish forloren hare: a sliced oval meatloaf roll wrapped in crispy bacon, golden-brown, with brown gravy, boiled potatoes and red cabbage'),
    (r'hakkebøf', 'Danish hakkebøf med bløde løg: a thick rounded pan-fried beef patty topped with a heap of soft golden caramelised onions in glossy brown gravy, with boiled potatoes'),
    (r'karbonade', 'Danish karbonader: round pan-fried pork patties with brown onion gravy and boiled potatoes'),
    (r'brun kødsovs', 'Danish gammeldags brun kødsovs: a plate of whole boiled potatoes and boiled carrot pieces with a thick brown gravy of crumbled browned minced beef and onion spooned over, plain and homely'),
    (r'biksemad', 'Danish biksemad: fried diced potatoes and small meat pieces with onion, topped with a sunny-side-up fried egg, with pickled beetroot slices and parsley'),
    (r'brændende kærlighed', 'Danish brændende kærlighed: fluffy mashed potatoes topped with crispy fried bacon pieces and golden fried onions, with pickled beetroot on the side'),
    (r'æggekage', 'Danish æggekage: a thick golden baked egg cake cut in pieces with crispy bacon, served with tomato slices and dark rye bread'),
    (r'stuvet|stuvede', 'Danish stuvet kål: soft cabbage in a creamy white sauce with nutmeg, served with fried sausage and boiled potatoes'),
    (r'skipperlabskovs', 'Danish skipperlabskovs: thick beef and potato stew served with rye bread and pickled beetroot'),
    (r'gule ærter', 'Danish yellow pea soup (gule ærter) with pieces of pork and sausage in a deep bowl, mustard on the side'),
    (r'rugbrød|smørrebrød|madder', 'Danish smørrebrød: open-faced sandwiches on slices of dark rye bread, neatly garnished'),
    (r'kartoffel.*suppe|suppe', 'Creamy soup in a deep white bowl, topped with garnish, served with dark rye bread'),
    (r'helstegt and|and med|andebryst|andelår', 'Danish roast duck with golden crispy skin, apples and prunes, served with red cabbage, caramelised potatoes and brown gravy'),
    (r'helstegt kylling|hel kylling', 'Whole roasted chicken with golden crispy skin on a platter with roasted potatoes and carrots, gravy on the side'),
    (r'kylling i karry', 'Danish kylling i karry: chicken pieces in a creamy yellow curry sauce with apple, served with white rice'),
    (r'koteletter|svinekotelet', 'Pan-fried golden pork chops with creamy gravy, served with boiled potatoes'),
    (r'mørbrad', 'Sliced pork tenderloin, pink and juicy, with gravy and boiled potatoes'),
    (r'bøffer? med champignonsovs|champignonsovs', 'Danish bøf med champignonsovs: whole pan-fried beef steaks, evenly browned and cooked through (not sliced, no raw meat visible), covered with a creamy light-brown mushroom sauce with sliced champignons, served with boiled potatoes and parsley'),
    (r'oksegryde|gullasch', 'Slow-cooked beef stew with tender chunks of meat and root vegetables in a rich brown sauce'),
    (r'entrecote|oksebøf|steak|cuvette|schnitzel', 'Pan-seared steak sliced to show a pink centre, with baked potato wedges and sauce'),
    (r'laks|fisk i fad|ovnbagt fisk|torsk|sej', 'Pan-seared or baked fish fillet, flaky and moist, with lemon, fresh dill and boiled potatoes'),
    # italiensk
    (r'carbonara', 'Italian spaghetti carbonara: glossy creamy egg sauce coating the spaghetti, crispy bacon pieces, lots of black pepper and pecorino'),
    (r'bolognese|(?<!brun )kødsovs', 'Italian spaghetti with a rich slow-cooked meat ragù, topped with freshly grated parmesan and a basil leaf'),
    (r'lasagne', 'Italian lasagne in a baking dish, layered pasta with meat ragù and bubbling golden cheese, a square portion lifted out'),
    (r'pizza', 'Italian homemade pizza with a thin crust with blistered golden edges, melted cheese and toppings'),
    (r'risotto', 'Creamy Italian risotto with a glossy texture, served in a shallow bowl with parmesan'),
    (r'parmigiana', 'Italian chicken parmigiana: golden breaded cutlet covered in tomato sauce and melted mozzarella with basil'),
    # amerikansk
    (r'burger(?!-?pasta)', 'Homemade burger in a toasted bun with a juicy patty, melted cheese, lettuce and tomato, served on a wooden board'),
    (r'tacos|fajita|burrito|quesadilla|wraps', 'Tex-Mex dish with warm tortillas, seasoned filling, fresh salad, tomato and sour cream'),
    (r'mac and cheese', 'Creamy baked macaroni and cheese with a golden cheesy crust and crispy bacon'),
    (r'chili', 'Hearty chili con carne in a bowl with rice, topped with sour cream and chopped chili'),
    (r'ribs|spareribs', 'Sticky glazed pork ribs, glossy dark brown, with corn and coleslaw'),
    # asiatisk
    (r'sød-sur', 'Chinese-style sweet and sour chicken with vegetables in a glossy red-orange sauce, with white rice in a bowl'),
    (r'wok|nudler|stegt ris|teriyaki|satay|koreansk', 'Asian stir-fry in a bowl with vegetables and meat, glossy sauce, chopsticks on the side'),
    (r'karry|tikka|kokos', 'Creamy curry in a bowl with tender pieces and rice, garnished with fresh coriander'),
    # middelhav
    (r'gyros|pita|tzatziki|falafel|græsk', 'Greek dish with warm pita bread, tzatziki, tomato, cucumber and feta, served on a stoneware plate'),
    (r'shakshuka|moussaka|couscous|halloumi', 'Mediterranean dish in a skillet or baking dish with tomatoes, herbs and olive oil'),
]


def detalje(navn):
    n = navn.lower()
    for mønster, tekst in DETALJER:
        if re.search(mønster, n):
            return tekst
    return None


def byg_prompt(navn, koekken, besk=None):
    """Den samlede prompt: faglig beskrivelse (eller den håndskrevne), køkkenstil og nordisk fotostil."""
    kerne = detalje(navn)
    if kerne and besk:
        kerne = f'{kerne}. Dish: {besk}'
    elif not kerne:
        kerne = besk or navn
    return f'{kerne}. {STIL_KOEKKEN.get(koekken, "")}. {STIL_NORDISK}'

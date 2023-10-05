import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bullet.settings")
import django
django.setup()

from bullet import search
import json
from datetime import timedelta

from django.db import transaction

from competitions.branches import Branches
from competitions.models import Competition, Category, Venue
from education.models import School
from problems.models import SolvedProblem, Problem, CategoryProblem, ResultRow
from users.models import Team

countries = {'1': 'SK', '2': 'CZ', '4': 'DE', '6': 'FI', '7': 'PL', '8': 'AT', '9': 'HU', '10': 'GB', '11': 'RO', '12': 'RU', '13': 'CH', '14': 'IR', '15': 'UA', '16': 'BY', '17': 'OP', '18': 'FR', '19': 'NL', '20': 'EE'}
sites = {'1': ('Praha', '2', 'PHA'), '2': ('Bratislava', '1', 'BA'), '3': ('Opava', '2', 'OPA'), '4': ('Košice', '1', 'KE'), '6': ('Praha - DE', '4', 'DE'), '8': ('Nitra', '1', 'NR'), '9': ('Oulu', '6', 'OUL'), '10': ('Passau', '4', 'PAS'), '11': ('Brno', '2', 'BO'), '12': ('Třebíč', '2', 'TR'), '13': ('Praha Doppler', '2', 'PHA D'), '14': ('Praha Voděradská', '2', 'PHA V'), '15': ('Karlovy Vary', '2', 'KV'), '16': ('Hradec Králové', '2', 'HK'), '17': ('Česká Lípa', '2', 'CL'), '18': ('České Budějovice', '2', 'CB'), '20': ('Olomouc', '2', 'OC'), '21': ('Ostrava', '2', 'OVA'), '22': ('Hlohovec', '1', 'HC'), '23': ('Lučenec', '1', 'LC'), '24': ('Námestovo', '1', 'NO'), '25': ('Žilina', '1', 'ZA'), '26': ('Poprad', '1', 'PP'), '27': ('Partizánske', '1', 'PE'), '28': ('Púchov', '1', 'PU'), '29': ('Brezno', '1', 'BR'), '30': ('Trstená', '1', 'TS'), '31': ('Banská Bystrica', '1', 'BB'), '32': ('Šurany', '1', 'SR'), '33': ('Dolný Kubín', '1', 'DK'), '34': ('Michalovce', '1', 'MI'), '35': ('Bílovec', '2', 'BIL'), '36': ('Kraków', '7', 'KR'), '37': ('Linz', '8', 'LZ'), '38': ('Budapest', '9', 'BUD'), '39': ('Warszawa', '7', 'WAR'), '40': ('Wrocław', '7', 'WRO'), '41': ('Gdynia', '7', 'GA'), '42': ('Písek', '2', 'PS'), '43': ('Frýdlant nad Ostravicí', '2', 'FNO'), '45': ('Zlín', '2', 'ZL'), '46': ('Prešov', '1', 'PO'), '47': ('Trenčín', '1', 'TN'), '48': ('Levice', '1', 'LV'), '49': ('Veszprém', '9', 'VE'), '50': ('Plzeň', '2', 'PZ'), '51': ('Ústí nad Labem', '2', 'UL'), '53': ('Sokolov', '2', 'SO'), '54': ('Bánovce nad Bebravou', '1', 'BN'), '55': ('Dubnica nad Váhom', '1', 'DU'), '56': ('Liptovský Mikuláš', '1', 'LM'), '57': ('Piešťany', '1', 'PN'), '58': ('Prievidza', '1', 'PD'), '59': ('Spišská Nová Ves', '1', 'SN'), '60': ('Sučany', '1', 'SU'), '61': ('Šahy', '1', 'SH'), '62': ('Zvolen', '1', 'ZV'), '63': ('Gdańsk', '7', 'GD'), '64': ('Edinburgh', '10', 'ED'), '65': ('Kadaň', '2', 'KA'), '66': ('Trnava', '1', 'TT'), '67': ('Bielsko-Biała', '7', 'BIE'), '69': ('Krosno', '7', 'KRO'), '70': ('Sosnowiec', '7', 'SOS'), '71': ('Tarnów', '7', 'TAR'), '73': ('Grodzisk Mazowiecki', '7', 'GRO'), '74': ('Białystok', '7', 'BIA'), '75': ('Constanța', '11', 'CON'), '76': ('Liberec', '2', 'LB'), '77': ('Москва', '12', 'MOS'), '78': ('Łódź', '7', 'LOD'), '83': ('Zürich', '13', 'ZH'), '84': ('Cambridge', '10', 'CAM'), '85': ('Новосибирск', '12', 'NVS'), '86': ('Pardubice', '2', 'PC'), '87': ('Rzeszów', '7', 'RZ'), '88': ('Wien', '8', 'WI'), '89': ('Київ', '15', 'KY'), '90': ('Bytča', '1', 'BY'), '91': ('Leipzig', '4', 'LPZ'), '92': ('Glasgow', '10', 'GLA'), '93': ('Гомель', '16', 'GOM'), '94': ('Česká republika online', '2', 'CZON'), '95': ('Slovensko online', '1', 'SKON'), '96': ('Polska online', '7', 'PLON'), '97': ('Magyarország online', '9', 'HUON'), '98': ('Россия online', '12', 'RUON'), '99': ('Deutschland Online', '4', 'DEON'), '100': ('UK Online', '10', 'GBON'), '101': ('Romania online', '11', 'ROON'), '102': ('Schweiz Online', '13', 'CHON'), '103': ('Open', '17', 'OPEN'), '104': ('Österreich online', '8', 'ATON'), '105': ('Iran Online', '14', 'IRON'), '106': ('Беларусь Online', '16', 'BYON'), '107': ('France online', '18', 'FRON'), '108': ('Nederland online', '19', 'NLON'), '109': ('Eesti online', '20', 'EEON'), '110': ('Innsbruck', '8', 'IN'), '111': ('Villach', '8', 'VIL'), '112': ('Tallinn', '20', 'TAL'), '113': ('Tartu', '20', 'TAR'), '114': ('Tehran', '14', 'TEH')}

countries = {int(k): v for k,v in countries.items()}
sites = {int(k): v for k,v in sites.items()}

ROCNIK = 240

"""
SELECT school.*, region.id_country FROM `school` JOIN district ON district.id_district=school.id_district JOIN region on region.id_region = district.id_region
"""
with open("_dat/school.json") as f:
    schools = json.load(f)
    schools = {s["id_school"]: s for s in schools}

# -------------

"""
SELECT * FROM competition WHERE id_competition = 89;
"""
with open("_dat/competition.json") as f:
    competition = json.load(f)[0]

"""
SELECT * from site_of_competition WHERE id_category != 4 and id_competition = 89;
"""
with open("_dat/site_of_competition.json") as f:
    venues = json.load(f)

"""
SELECT team.* FROM `team` JOIN site_of_competition ON site_of_competition.id_site_of_competition = team.id_site_of_competition WHERE site_of_competition.id_category != 4 and site_of_competition.id_competition = 45 AND state = 'registered'
"""
with open("_dat/team.json") as f:
    teams = json.load(f)

"""
SELECT solved.*, problem_in_competition.number, problem_in_competition.id_problem FROM `solved` JOIN team on solved.id_team = team.id_team join site_of_competition on team.id_site_of_competition = site_of_competition.id_site_of_competition join problem_in_competition on problem_in_competition.id_problem_in_competition = solved.id_problem_in_competition where site_of_competition.id_category != 4 and site_of_competition.id_competition = 45;
"""
with open("_dat/solved.json") as f:
    solved = json.load(f)


with transaction.atomic():
    search.enabled = False
    branch = int(competition["id_branch"])
    if branch >= 3:
        branch = 3
    c = Competition.objects.create(
        name=competition["name"],
        branch=Branches[branch],
        number=ROCNIK,
        web_start=competition["web_start"],
        registration_start=competition["registration_start"],
        registration_second_round_start=competition["registration_second_round"],
        registration_end=competition["registration_end"],
        competition_start=competition["competition_start"],
        competition_duration=competition["competition_duration"],
        results_freeze="00:00:00",
        results_public=True,
    )
    #
    cats = {
        1: Category.objects.create(competition=c, identifier="senior", order=2, problems_per_team=0, max_teams_per_school=0, max_teams_second_round=0, max_members_per_team=10),
        2: Category.objects.create(competition=c, identifier="junior", order=1, problems_per_team=0, max_teams_per_school=0, max_teams_second_round=0, max_members_per_team=10),
    }
    #
    vens = {
        v["id_site_of_competition"]: Venue.objects.create(
            name=sites[v["id_site"]][0],
            shortcode=sites[v["id_site"]][2].replace(" ", "") + cats[v["id_category"]].identifier[0].upper(),
            country=countries[v["id_country"]],
            category=cats[v["id_category"]],
            accepted_languages=[],
            is_reviewed=True,
        )
        for v in venues
    }
    #
    team_objs = {}
    for t in teams:
        sch_data = schools[t["id_school"]]
        sch, _ = School.objects.get_or_create(importer="legacy", importer_identifier=t["id_school"], defaults={
            "name": sch_data["name"],
            "address": f"{sch_data['street']}, {sch_data['city']}",
            "country": countries[sch_data["id_country"]]
        })
        team_objs[t["id_team"]] = Team.objects.create(
            contact_name="Redacted",
            contact_email="redacted@naboj.org",
            school=sch,
            language="en",
            registered_at=t["request_time"],
            confirmed_at=t["confirmation_time"],
            venue=vens[t["id_site_of_competition"]],
            number=t["number"],
            in_school_symbol=t["symbol"],
            is_checked_in=True,
            is_reviewed=True,
        )
    #
    for s in solved:
        if not s["valid"]:
            continue
        prob, created = Problem.objects.get_or_create(competition=c, name=s["id_problem"])
        if created:
            for cat in cats.values():
                CategoryProblem.objects.create(problem=prob, category=cat, number=s["number"])
        SolvedProblem.objects.create(
            team=team_objs[s["id_team"]],
            competition_time=timedelta(seconds=s["time_elapsed"]),
            problem=prob,
        )

    for team in team_objs.values():
        problems = SolvedProblem.objects.filter(team=team).values_list("problem").order_by("-competition_time")
        last_problem = SolvedProblem.objects.filter(team=team).order_by("-competition_time").first()
        solved_problems = set(
            CategoryProblem.objects.filter(
                problem__in=problems, category=team.venue.category
            ).values_list("number", flat=True)
        )
        if not last_problem:
            continue
        result_row = ResultRow()
        result_row.team = team
        result_row.solved_count = len(solved_problems)
        solved_bin = 0
        for p in solved_problems:
            solved_bin |= 1 << (p - 1)
        result_row.solved_problems = solved_bin.to_bytes(16, "big")
        result_row.competition_time = last_problem.competition_time + timedelta(seconds=1)
        result_row.save()


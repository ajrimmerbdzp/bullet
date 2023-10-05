# competition.json
SELECT * FROM competition WHERE id_competition = 89;
# site_of_competition.json
SELECT * from site_of_competition WHERE id_category != 4 and id_competition = 89;
# team.json
SELECT team.* FROM `team` JOIN site_of_competition ON site_of_competition.id_site_of_competition = team.id_site_of_competition WHERE site_of_competition.id_category != 4 and site_of_competition.id_competition = 89 AND state = 'registered';
# solved.json
SELECT solved.*, problem_in_competition.number, problem_in_competition.id_problem FROM `solved` JOIN team on solved.id_team = team.id_team join site_of_competition on team.id_site_of_competition = site_of_competition.id_site_of_competition join problem_in_competition on problem_in_competition.id_problem_in_competition = solved.id_problem_in_competition where site_of_competition.id_category != 4 and site_of_competition.id_competition = 89;

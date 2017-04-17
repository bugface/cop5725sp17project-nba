<<<<<<< HEAD
select * from
(select player_name, ROUND(AVG(pts),2) as points_avg from STATS where  date_ BETWEEN '01-OCT-09' and '01-JUL-10'
group by player_id, player_name order by points_avg desc) where rownum <6;

select * from
(select player_name, ROUND(AVG(TRB),2) as rebounds_avg from STATS where  date_ BETWEEN '01-OCT-09' and '01-JUL-10'
group by player_id, player_name order by rebounds_avg desc) where rownum <6;

select * from
(select player_name, ROUND(AVG(ast),2) as assists_avg from STATS where  date_ BETWEEN '01-OCT-09' and '01-JUL-10'
group by player_id, player_name order by assists_avg desc) where rownum <6;

-- average statistics of players come from university of florida
select player_name, players.height, ROUND(AVG(pts),2) as points_avg, ROUND(AVG(TRB),2) as rebounds_avg, ROUND(AVG(ast),2) as assists_avg from STATS, Players
where STATS.player_id=Players.player_id and Players.college='University of Florida'
group by stats.player_id, stats.player_name, players.height order by points_avg desc, rebounds_avg desc, assists_avg desc;

-- players and his court position that 3p percentage is larger than 40% and made more than 400 3 pointers
select player_name, players.POS, sum(FG3) as threep_made,ROUND((sum(FG3)/sum(FG3A)),4) as threep_percent from stats, players
where STATS.player_id=Players.player_id
group by stats.player_id, stats.player_name, players.POS
having sum(FG3A)>0 and sum(FG3)>400 and (sum(FG3)/sum(FG3A))> 0.4
order by threep_made desc, threep_percent desc;

-- show the game winning numbers and the coach in a perticular season
select coach.name as coach, team.name as team, count(games.WIN_TEAM) as win from  games, team, coach
where games.gamedate BETWEEN '01-OCT-09' and '01-JUL-10' and coach.year='2009-10'
and team.TEAM_NAME_ABBR= games.win_team and coach.TEAM=team.TEAM_NAME_ABBR
group by games.WIN_TEAM, team.name, coach.name
order by win desc;

select sum(tuples) from ((select count(*) as tuples from stats) union (select count(*) as tuples from coach));
=======
select * from
(select player_name, ROUND(AVG(pts),2) as points_avg from STATS where  date_ BETWEEN '01-OCT-09' and '01-JUL-10'
group by player_id, player_name order by points_avg desc) where rownum <6;

select * from
(select player_name, ROUND(AVG(TRB),2) as rebounds_avg from STATS where  date_ BETWEEN '01-OCT-09' and '01-JUL-10'
group by player_id, player_name order by rebounds_avg desc) where rownum <6;

select * from
(select player_name, ROUND(AVG(ast),2) as assists_avg from STATS where  date_ BETWEEN '01-OCT-09' and '01-JUL-10'
group by player_id, player_name order by assists_avg desc) where rownum <6;​





select * from
(select player_name, ROUND(AVG(pts),2) as points_avg from STATS where  date_ BETWEEN '01-OCT-09' and '01-JUL-10'
group by player_id, player_name order by points_avg desc) where rownum <6;

select * from
(select player_name, ROUND(AVG(TRB),2) as rebounds_avg from STATS where  date_ BETWEEN '01-OCT-09' and '01-JUL-10'
group by player_id, player_name order by rebounds_avg desc) where rownum <6;

select * from
(select player_name, ROUND(AVG(ast),2) as assists_avg from STATS where  date_ BETWEEN '01-OCT-09' and '01-JUL-10'
group by player_id, player_name order by assists_avg desc) where rownum <6;

-- average statistics of players come from university of florida
select player_name, players.height, ROUND(AVG(pts),2) as points_avg, ROUND(AVG(TRB),2) as rebounds_avg, ROUND(AVG(ast),2) as assists_avg from STATS, Players
where STATS.player_id=Players.player_id and Players.college='University of Florida'
group by stats.player_id, stats.player_name, players.height order by points_avg desc, rebounds_avg desc, assists_avg desc;

-- players and his court position that 3p percentage is larger than 40% and made more than 400 3 pointers
select player_name, stats.PLAYER_ID, players.POS, sum(FG3) as threep_made,ROUND((sum(FG3)/sum(FG3A)),4) as threep_percent from stats, players
where STATS.player_id=Players.player_id
group by stats.player_id, stats.player_name, players.POS
having sum(FG3A)>0 and sum(FG3)>400 and (sum(FG3)/sum(FG3A))> 0.4
order by threep_made desc, threep_percent desc;

-- show the game winning numbers and the coach in a perticular season
select coach.name as coach, team.name as team, count(games.WIN_TEAM) as win from  games, team, coach
where games.gamedate BETWEEN '01-OCT-09' and '01-JUL-10' and coach.year='2009-10'
and team.TEAM_NAME_ABBR= games.win_team and coach.TEAM=team.TEAM_NAME_ABBR
group by games.WIN_TEAM, team.name, coach.name
order by win desc;

-- highest score of each season for a single player and his age
select * from (select distinct stats.player_name, ROUND(months_between(date_, birthdate )/12,0) as age, max(pts)
from stats, players
where STATS.player_id=Players.player_id and date_ BETWEEN '01-OCT-09' and '01-JUL-10'
group by stats.player_id, stats.player_name, ROUND(months_between(date_, birthdate )/12,0)
order by max(pts) desc, age asc) where rownum<11;

-- players in university of florida who have won championship in NBA
select distinct players.NAME, team.name as T_name, s_id from players, seasons, team, stats
  where (
  ((seasons.champion= team.name and team.team_name_abbr= stats.team) and (date_ BETWEEN '01-OCT-08' and '01-JUL-09'and s_id= '2008-09')) or
  ((seasons.champion= team.name and team.team_name_abbr= stats.team) and (date_ BETWEEN '01-OCT-09' and '01-JUL-10'and s_id= '2009-10')) or
  ((seasons.champion= team.name and team.team_name_abbr= stats.team) and (date_ BETWEEN '01-OCT-10' and '01-JUL-11'and s_id= '2010-11')) or
  ((seasons.champion= team.name and team.team_name_abbr= stats.team) and (date_ BETWEEN '01-OCT-11' and '01-JUL-12'and s_id= '2011-12')) or
  ((seasons.champion= team.name and team.team_name_abbr= stats.team) and (date_ BETWEEN '01-OCT-12' and '01-JUL-13'and s_id= '2012-13'))
)and Players.college='University of Florida' and players.PLAYER_ID= stats.player_id order by s_id desc;

-- college list
select distinct college from players where college is not null;

select sum(tuples) from ((select count(*) as tuples from stats) union (select count(*) as tuples from coach));

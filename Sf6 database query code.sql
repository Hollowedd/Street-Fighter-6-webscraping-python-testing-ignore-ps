--basic overview of databse
select character_name, rating,[fighter_banner_info personal_info platform_name],[fighter_banner_info home_name]
from [SF6 Data]..finished_ranking_csv
where rating != 36 and cast(rating as numeric) > 1000 
order by rating desc

-- testing just japan
SELECT COUNT(*) AS JapanCount
FROM [SF6 Data]..finished_ranking_csv
WHERE [fighter_banner_info home_name] = 'Japan';

--all countires
Select [fighter_banner_info home_name], COUNT(*) as CountryCount  
FROM [SF6 Data]..finished_ranking_csv
where [fighter_banner_info home_name] NOT LIKE '%[0-9]%'
group by [fighter_banner_info home_name]
order by CountryCount desc

--looking at overall characters
Select character_name, COUNT(*) as CharCount	   
FROM [SF6 Data]..finished_ranking_csv
where (character_name != 'Steam' and character_name != 'CrossPlatform')
group by character_name
order by CharCount desc


Select [fighter_banner_info personal_info platform_name], COUNT(*) as PlatForm	   
FROM [SF6 Data]..finished_ranking_csv
where [fighter_banner_info personal_info platform_name] like '%Steam%' or [fighter_banner_info personal_info platform_name] like '%CrossPlatform'
group by [fighter_banner_info personal_info platform_name]
order by [fighter_banner_info personal_info platform_name] asc


Select [fighter_banner_info home_name], character_name, COUNT(*) as CharacterCount	   
FROM [SF6 Data]..finished_ranking_csv
--where [fighter_banner_info home_name] not like '%1%'
group by [fighter_banner_info home_name], character_name
order by [fighter_banner_info home_name], character_name desc


With RankedCharacters as (
	Select 
		[fighter_banner_info home_name], 
		character_name, 
		COUNT(*) as CharacterCount,
		ROW_NUMBER() over (partition by [fighter_banner_info home_name] order by count(*) desc) as Rank
	FROM [SF6 Data]..finished_ranking_csv
	group by [fighter_banner_info home_name], character_name
	)
SELECT [fighter_banner_info home_name], character_name, CharacterCount, Rank
FROM RankedCharacters
where [fighter_banner_info home_name] NOT LIKE '%[0-9]%' and Rank < 6
ORDER BY [fighter_banner_info home_name] DESC;

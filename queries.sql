-- 1.Top 10 best-selling games worldwide
select g.game_name, SUM(rs.num_sales) as total_sales
from game as g 
join game_publisher as gpub on g.id = gpub.game_id
join game_platform as gplat on gpub.id = gplat.game_publisher_id
join region_sales rs on gplat.id = rs.game_platform_id
group by g.game_name
order by total_sales desc
limit 10

-- 2.Top 3 regions with highest-selling games
select r.region_name, sum(rs.num_sales) as total_sales
from region as r
join region_sales as rs on r.id = rs.region_id
group by r.region_name
order by total_sales DESC
limit 3


-- 3.Genres by sales
select ge.genre_name, sum(rs.num_sales) as total_sales
from genre as ge
join game as g on ge.id = g.genre_id
join game_publisher as gpub on g.id = gpub.game_id
join game_platform as gplat on gpub.id = gplat.game_publisher_id
join region_sales as rs on gplat.id = rs.game_platform_id
group by ge.genre_name
order by total_sales desc


-- 4.How many games belong to each genre
select ge.genre_name, count(g.id) as game_count
from genre as ge 
join game as g on ge.id = g.genre_id
group by ge.genre_name
order by game_count desc


-- 5.Publishers by sales
select p.publisher_name, sum(rs.num_sales) as total_sales
from publisher as p
join game_platform as gplat on p.id = gplat.game_publisher_id
join region_sales as rs on gplat.id = rs.game_platform_id
group by p.publisher_name
order by total_sales desc
limit 10

-- 6.Yearly sales
select gplat.release_year, sum(rs.num_sales) as total_sales
from game_platform as gplat
join region_sales as rs on gplat.id = rs.game_platform_id
group by gplat.release_year
order by gplat.release_year

-- 7.Platforms by total sales
select pl.platform_name, sum(rs.num_sales) as total_sales
from platform as pl
join game_platform as gplat on pl.id = gplat.platform_id
join region_sales as rs on gplat.id = rs.game_platform_id
group by pl.platform_name
order by total_sales desc

-- 8.Best-selling genre in each region
select region_name, genre_name, total_sales
from (
    select r.region_name, ge.genre_name, sum(rs.num_sales) as total_sales,
           row_number() over (partition by r.region_name order by sum(rs.num_sales) desc) as rn
    from region as r
    join region_sales as rs on r.id = rs.region_id
    join game_platform as gplat on rs.game_platform_id = gplat.id
    join game_publisher as gpub on gplat.game_publisher_id = gpub.id
    join game as g on gpub.game_id = g.id
    join genre as ge on g.genre_id = ge.id
    group by r.region_name, ge.genre_name
) ranked
where rn = 1
order by total_sales desc

-- 9.Platforms by game count
select p.platform_name, count(distinct g.id) as game_count
from platform as p
join game_platform as gplat on p.id = gplat.platform_id
join game_publisher as gpub on gplat.game_publisher_id = gpub.id
join game as g on gpub.game_id = g.id
group by p.platform_name
order by game_count desc

-- 10.Cumulative global sales over time
select gplat.release_year,
       sum(sum(rs.num_sales)) over (order by gplat.release_year) as cumulative_sales
from game_platform as gplat
join region_sales as rs on gplat.id = rs.game_platform_id
group by gplat.release_year
order by gplat.release_year







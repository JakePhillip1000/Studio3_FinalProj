-- This one I select all the components from the db
SELECT "firstName", "lastName" FROM athletes;

/*
    WHAT if I want to select specific columns?
    and match the exact values? This will select only the one who name is Jake
*/
SELECT * FROM athletes WHERE "firstName" = 'Jake';

-- Names ending with p
SELECT * FROM athletes WHERE "firstName" LIKE '%p';

-- Names starting with p
SELECT * FROM athletes WHERE "firstName" LIKE 'p%';

-- lastname containing ja
SELECT * FROM athletes WHERE "lastName" LIKE '%ja%';

/*
    AND, OR Operators. And is like union in set notation, but
    OR is like intersection in set notation
*/
SELECT * FROM athletes WHERE gender = 'Men' AND country = 'TH';
SELECT * FROM athletes WHERE "dateOfBirth" < '2006-01-01' OR country = 'USA';

/*Get only first 3 athletes*/
SELECT * FROM athletes LIMIT 3;

-- Counting the total athletes by country
SELECT country, COUNT(*) AS total_athletes FROM athletes
GROUP BY country
ORDER BY total_athletes DESC;

-- Finding youngest and oldest athletes in db
SELECT 
    MIN("dateOfBirth") AS oldest,
    MAX("dateOfBirth") AS youngest
FROM athletes;

/*
    Classifying athletes into group of ages
*/

SELECT 
    "firstName", "lastName", "dateOfBirth",
    CASE
        WHEN "dateOfBirth" >= '2010-01-01' THEN 'Under 15'
        WHEN "dateOfBirth" BETWEEN '2000-01-01' AND '2009-12-31' THEN '15-24'
        WHEN "dateOfBirth" BETWEEN '1990-01-01' AND '1999-12-31' THEN '25-34'
        ELSE '35+ or older'
    END AS grouping_age FROM athletes
ORDER BY grouping_age, "firstName";


-- Top 3 youngest athletes in each country
SELECT * FROM (
    SELECT id, "firstName", "lastName", country, "dateOfBirth",
        ROW_NUMBER() OVER (PARTITION BY country ORDER BY "dateOfBirth" DESC) AS rank FROM athletes
) 
AS ranked WHERE rank <= 3;


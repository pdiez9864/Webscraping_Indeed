-- Query intoduccion
SELECT puesto, "compañia" 
FROM "grupo3-indeed-tfm-webdata-dev"."indeedscrap"
ORDER BY "compañia" 
LIMIT 5;


-- Queremos ver cuanto lleva publicado en cada empresa para saber cual es la que mas tarda
SELECT DISTINCT "compañia", publicado 
FROM "grupo3-indeed-tfm-webdata-dev"."indeedscrap" 
ORDER BY "compañia";
LIMIT 5;

-- Queremos saber cuanto duran las candidaturas
SELECT publicado, COUNT(publicado) AS "total" 
FROM "grupo3-indeed-tfm-webdata-dev"."indeedscrap" 
GROUP BY publicado 
ORDER BY total DESC 
LIMIT 5;


-- Compañia que mas solicita
SELECT "compañia", COUNT("compañia") AS "total" 
FROM "grupo3-indeed-tfm-webdata-dev"."indeedscrap" 
GROUP BY "compañia" 
ORDER BY total DESC 
LIMIT 5;


-- Que solicita dicha compañia
SELECT puesto,"compañia" 
FROM "grupo3-indeed-tfm-webdata-dev"."indeedscrap" 
WHERE "compañia"='Tecnoempleo'
ORDER BY "compañia" 
LIMIT 5;


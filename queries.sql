-- Queries para análise dos dados de saúde

-- 1. Contagem de pacientes por classificação de IMC
SELECT classificacao_imc, COUNT(*) AS total
FROM pacientes
GROUP BY classificacao_imc;

-- 2. Contagem de pacientes com e sem doenças cardiovasculares
SELECT cardio, COUNT(*) AS total
FROM pacientes
GROUP BY cardio;

-- 3. Média de IMC por gênero
SELECT gender,
       ROUND(AVG(imc), 2) AS imc_medio
FROM pacientes
GROUP BY gender;

-- 4. Percentual de pacientes com obesidade
SELECT ROUND(AVG(imc), 2) AS imc_medio
FROM pacientes;

-- 5. Contagem de pacientes com obesidade por gênero
SELECT
    gender,
    classificacao_imc,
    COUNT(*) AS total
FROM pacientes
WHERE classificacao_imc = 'Obesidade'
GROUP BY gender;

-- 6. Percentual de pacientes com doenças cardiovasculares
SELECT
    ROUND(
        COUNT(
            CASE WHEN cardio = 1 THEN 1 END
        ) * 100.0 /
        COUNT(*),
        2
    ) AS percentual_cardio
FROM pacientes;

-- 7. Contagem de pacientes por classificação de IMC e presença de doenças cardiovasculares
SELECT
    classificacao_imc,
    cardio,
    COUNT(*) AS total
FROM pacientes
GROUP BY classificacao_imc, cardio
ORDER BY total DESC;

-- 8. Percentual de pacientes com obesidade
SELECT
    ROUND(
        COUNT(
            CASE
            WHEN classificacao_imc = 'obesidade' then 1
            end     
        ) * 100.0 / COUNT(*), 2
    ) AS percentual_obesidade
FROM pacientes;

--9. Cardiopatia por classificação de IMC
SELECT
    classificacao_imc,
    cardio,
    COUNT(*) AS total
FROM pacientes
GROUP BY classificacao_imc, cardio
ORDER BY total DESC;

--10. Colesterol x Doença Cardiovascular
select
    cholesterol,
    cardio,
    count(*) as total
from pacientes
group by cholesterol, cardio
order by cholesterol desc;

--11. Glicose x Doença Cardiovascular
SELECT
    gluc,
    cardio,
    COUNT(*) AS total
FROM pacientes
GROUP BY gluc, cardio
ORDER BY gluc;

--12. Fumante x Doença Cardiovascular
SELECT
    smoke,
    cardio,
    COUNT(*) AS total
FROM pacientes
GROUP BY smoke, cardio;

--13. Consumo de álcool x Doença Cardiovascular
SELECT
    alco,
    cardio,
    COUNT(*) AS total
FROM pacientes
GROUP BY alco, cardio;

--14. Atividade física x Doença Cardiovascular
SELECT
    active,
    cardio,
    COUNT(*) AS total
FROM pacientes
GROUP BY active, cardio;

--15. Faixa etária x Doença Cardiovascular
SELECT
    CASE
        WHEN age < 30 THEN 'Até 30'
        WHEN age < 40 THEN '31-40'
        WHEN age < 50 THEN '41-50'
        WHEN age < 60 THEN '51-60'
        ELSE '60+'
    END AS faixa_etaria,
    COUNT(*) AS total
FROM pacientes
GROUP BY faixa_etaria;
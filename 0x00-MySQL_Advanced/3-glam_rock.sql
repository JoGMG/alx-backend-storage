-- Write a SQL script that lists all bands with `Glam rock` as their main style, ranked by their longevity

-- Requirements:

-- • Import this table dump: https://intranet.alxswe.com/rltoken/uPn947gnZLaa0FJrrAFTGQ
-- • Column names must be: `band_name` and `lifespan` (in years until 2022 - please use `2022` instead of `YEAR(CURDATE())`)
-- • You should use attributes `formed` and `split` for computing the `lifespan`
-- • Your script can be executed on any database
USE metal_bands
SELECT band_name, (IFNULL(split, '2020') - formed) AS lifespan
FROM metal_bands
WHERE FIND_IN_SET('Glam rock', IFNULL(style, "")) > 0
ORDER BY lifespan DESC;

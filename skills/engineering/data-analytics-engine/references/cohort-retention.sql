-- Portable cohort calculation. Normalize source timestamps into month indices
-- FIRST using the contract's timezone: year * 12 + month (any common origin).
-- user_cohort(user_id, cohort_month): fixed acquisition cohort membership.
-- activity_months(user_id, activity_month): approved qualifying activity.
-- reporting_months(month_index, is_complete): 1 only after full local-period
-- coverage is established. Missing rows do not prove a period is complete.
WITH cohort_sizes AS (
    SELECT cohort_month, COUNT(DISTINCT user_id) AS cohort_size
    FROM user_cohort
    GROUP BY cohort_month
)
SELECT
    c.cohort_month,
    p.month_index - c.cohort_month AS months_since_signup,
    COUNT(DISTINCT a.user_id) AS retained_customers,
    c.cohort_size,
    CASE WHEN p.is_complete = 1
         THEN COUNT(DISTINCT a.user_id) * 1.0 / NULLIF(c.cohort_size, 0)
         ELSE NULL
    END AS retention_rate
FROM cohort_sizes c
CROSS JOIN reporting_months p
JOIN user_cohort u ON u.cohort_month = c.cohort_month
LEFT JOIN activity_months a
    ON a.user_id = u.user_id AND a.activity_month = p.month_index
WHERE p.month_index >= c.cohort_month
GROUP BY c.cohort_month, p.month_index, p.is_complete, c.cohort_size
ORDER BY c.cohort_month, months_since_signup;

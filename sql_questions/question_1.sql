with base_query as (
    select *
    from (
        select d.department_id
            ,e.employee_id
            ,e.salary
            ,RANK() over (partition by d.department_id order by e.salary desc) as ranked_sal_department
        from departments d
        join employees e
            on e.department_id = d.department_id
    ) t
    where t.ranked_sal_department <= 2
)

select distinct b1.employee_id
    ,b1.salary
    ,b1.salary - b2.salary as sal_dif_from_second
from base_query b1
join base_query b2
    on b2.department_id = b1.department_id
    and b1.ranked_sal_department = 1 and b2.ranked_sal_department = 2
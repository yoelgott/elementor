with total_number_of_visitors as
(
    select v.site
        ,sum(number_of_visitors) as total_visitors
    from site_visitors v
    group by v.site
)
, on_promotion_dates as(
    select h.site
        ,sum(number_of_visitors) as sum_visitors
    from (
        select distinct v.site
            ,v.date
            ,v.number_of_visitors
            ,case when p.promotion_code is not null then 'promotion' else 'not_promotion' end as is_promotion_date
        from site_visitors v
        left join promotion_dates p
            on v.date between p.start_date and p.end_date
            and p.site = v.site
    ) h
    where h.is_promotion_date = 'promotion'
    group by h.site
)

select t.site
    ,(case when p.sum_visitors is null then 0 else p.sum_visitors / t.total_visitors) * 100 as percent_trafic_promotion_dates
from total_number_of_visitors t
left join on_promotion_dates p
    on t.site = p.site

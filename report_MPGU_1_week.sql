
--1. Статистика поданных заявлений через МПГУ за предыдущую неделю
select /*+ PARALLEL 8*/
l2.id as id_АЦ,
l2.name as наим_АЦ,
l.id as id_филиала,
l.name as наим_филиала,
count(case when are.attachment_request_status=10 then are.attachment_request_id end) as сохр_заявления,
(SELECT
 /*+ PARALLEL 8*/
 count (are1.attachment_request_id)
FROM attachment_request_event are1
join attachment_request ar1 on ar1.attachment_request_id = are1.attachment_request_id
where
ar1.source_attachment_request_id is not null
and are1.attachment_request_status=10 
and trunc(are1.change_date) >= trunc(SYSDATE -14) and trunc(are1.change_date) <= trunc(SYSDATE -8)
and are1.attachment_request_id not in
(select attachment_request_id from attachment_request_event
where attachment_request_status in (20,40,50)
and trunc(change_date) >= trunc(SYSDATE -14) and trunc(change_date) <= trunc(SYSDATE -1)   )
and ar1.lpu_id = l.id
) as ожид_заявл,
count(case when are.attachment_request_status=40 then are.attachment_request_id end) as прикр_заявления,
count(case when are.attachment_request_status=20 then are.attachment_request_id end) as отк_заявления,
count(case when are.attachment_request_status=50 then are.attachment_request_id end) as закр_заявления,
nvl(v.atp, 0) as действ_прикреп 
from attachment_request ar
join attachment_request_event are on are.attachment_request_id = ar.attachment_request_id
join lpu l on l.id = ar.lpu_id
left join lpu_group lg on lg.id = l.lpu_group_id
left join lpu l2 on l2.id = lg.main_lpu_id
left join
(
select
l2.id as acid1,
l2.name as наим_АЦ,
l.id as filid1,
l.name as наим_филиал,
nvl(count(distinct ar.attachment_request_id ) ,0) as atp
from attachment_request ar
join lpu l on l.id=ar.lpu_id
left join lpu_group lg on lg.id = l.lpu_group_id
left join lpu l2 on l2.id = lg.main_lpu_id
join attachment_request_event are on are.attachment_request_id = ar.attachment_request_id
join attachment_request ar2 on ar2.person_insurance_code = ar.person_insurance_code and ar2.attachment_request_id!=ar.attachment_request_id 
join attachment_request_event are2 on are2.attachment_request_id = ar2.attachment_request_id
join service_district sd on sd.id=ar2.service_district_id
join lpu_district_type ldt on ldt.id=sd.lpu_district_type and ldt.district_type=10
where 
ar.source_attachment_request_id is not null
and
(
trunc(are.change_date)>= trunc(SYSDATE -7) and trunc(are.change_date) <= trunc(SYSDATE -1) 
and are.attachment_request_status = 10
)
and
(
are2.attachment_request_status = 40
and are2.change_date<are.change_date
and  are2.change_date>= add_months(are.change_date,-12)
and
(
are2.attachment_request_status <> 50
or 
(are2.attachment_request_status = 50
and are2.change_date>are.change_date)
)
)
group by
l2.id,
l2.name,
l.id,
l.name
) v on l.id=v.filid1
where
ar.source_attachment_request_id is not null
and trunc(are.change_date)>= trunc(SYSDATE -7) and trunc(are.change_date) <= trunc(SYSDATE -1)
 group by
l2.id,
l2.name,
l.id,
l.name,
nvl(v.atp, 0)
order by l2.id



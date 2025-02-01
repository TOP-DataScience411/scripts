ins_departments = (
    'insert into departments '
    '  (name) '
    'values '
    '  (%s) '
)
ins_sponsors = (
    'insert into sponsors '
    '  (name) '
    'values '
    '  (%s) '
)
ins_specializations = (
    'insert into specializations '
    '  (name) '
    'values '
    '  (%s) '
)
ins_wards = (
    'insert into wards '
    '  (dep_id, name) '
    'values '
    '  (%s, %s) '
)
ins_donations = (
    'insert into donations '
    '  (sponsor_id, dep_id, date, amount) '
    'values '
    '  (%s, %s, %s, %s) '
)
ins_doctors = (
    'insert into doctors '
    '  (dep_id, last_name, first_name, patr_name, salary, premium) '
    'values '
    '  (%s, %s, %s, %s, %s, %s) '
)
ins_doctors_specs = (
    'insert into doctors_specs '
    '  (doctor_id, spec_id) '
    'values '
    '  (%s, %s) '
)
ins_vacations = (
    'insert into vacations '
    '  (doctor_id, start_date, end_date) '
    'values '
    '  (%s, %s, %s) '
)


sel_donations_by_year = '''
    select
      extract(year from "date") as year,
      sum(amount)
    from
      donations
    group by
      year
    order by
      year
'''

sel_donations_by_year_and_dep = '''
    select
      extract(year from "date") as year,
      dep_id,
      sum(amount)
    from
      donations
    group by
      year, 
      dep_id
    order by
      year,
      dep_id
'''

sel_count_week_vacations = '''
    select
      case when end_date - start_date <= 7 then 'неделя'
           else 'больше недели'
      end as week_or_more,
      count(*)
    from 
      vacations
    group by
      week_or_more
'''

sel_wards_departments = '''
    select 
      wards.name,
      departments.name
    from
      wards
    join
      departments on dep_id = departments.id
'''

sel_groupconcat_wards_departments = '''
      select d.name as "отделение",
             string_agg(w.name, ', ') as "палаты"
        from wards as w
        join departments as d
          on dep_id = d.id
    group by d.name
'''

sel_large_donations = '''
      select d.name as "отделение",
             s.name as "спонсор",
             date as "дата",
             amount as "сумма"
        from departments as d
        join donations
          on d.id = dep_id and d.id between 2 and 5
        join sponsors as s
          on sponsor_id = s.id and amount > 500000
    order by "отделение", "сумма"
'''

sel_all_doctors_specs = '''
       select concat_ws(' ', last_name, first_name, patr_name) as "ФИО",
              string_agg(s.name, ', ') as "Специальность"
         from doctors as d
    left join doctors_specs on d.id = doctor_id
    left join specializations as s on spec_id = s.id
     group by "ФИО"
     order by "ФИО"
'''

sel_doctors_cnt_for_spec = '''
        select s.name as "Специальность",
               count(doctor_id) as "Кол-во врачей"
          from doctors_specs
    right join specializations as s on spec_id = s.id
      group by s.name
      order by "Кол-во врачей" desc;
'''


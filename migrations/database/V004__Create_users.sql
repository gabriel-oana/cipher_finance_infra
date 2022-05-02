CREATE USER ${db_etl_user} PASSWORD '${db_etl_user_pw}' IN GROUP etl_group;
CREATE USER ${db_ro_user} PASSWORD '${db_ro_user_pw}' IN GROUP readonly_group;
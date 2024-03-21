import { createPool } from 'mysql2';
import { exit } from 'process';

let db_host = process.env.MYSQL_HOST;
if (db_host === undefined || db_host === "") {
    console.warn("MYSQL_HOST is not set");
    exit(1);
}

let db_user = process.env.MYSQL_USER;
if (db_user === undefined || db_user === "") {
    console.warn("MYSQL_USER is not set");
    exit(1);
}

let db_password = process.env.MYSQL_PASSWORD;
if (db_password === undefined || db_password === "") {
    console.warn("MYSQL_PASSWORD is not set");
    exit(1);
}

let db_name = process.env.MYSQL_DATABASE;
if (db_name === undefined || db_name === "") {
    console.warn("MYSQL_DATABASE is not set");
    exit(1);
}

export const connection = createPool({
    host: db_host,
    port: parseInt(process.env.MYSQL_PORT || '3306'),
    user: db_user,
    password: db_password,
    database: db_name
});
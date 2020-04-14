# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Airport data provided by David Megginson (http://ourairports.com/data/).

import csv
import io
import sqlalchemy

class Airports_Cloud_Sql(object):
  """An interface for reading data about airports."""

  def __init__(self, db_user, db_pass, db_name, cloud_sql_connection_name):
    print(db_user)
    print(db_pass)
    print(db_name)
    print(cloud_sql_connection_name)
    # [START cloud_sql_mysql_sqlalchemy_create]
    # The SQLAlchemy engine will help manage interactions, including automatically
    # managing a pool of connections to your database
    self.db = sqlalchemy.create_engine(
        # Equivalent URL:
        # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=/cloudsql/<cloud_sql_instance_name>
        sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username=db_user,
            password=db_pass,
            database=db_name,
            query={"unix_socket": "/cloudsql/{}".format(cloud_sql_connection_name)},
        ),
        # ... Specify additional properties here.
        # [START_EXCLUDE]
        # [START cloud_sql_mysql_sqlalchemy_limit]
        # Pool size is the maximum number of permanent connections to keep.
        pool_size=5,
        # Temporarily exceeds the set pool_size if no connections are available.
        max_overflow=2,
        # The total number of concurrent connections for your application will be
        # a total of pool_size and max_overflow.
        # [END cloud_sql_mysql_sqlalchemy_limit]
        # [START cloud_sql_mysql_sqlalchemy_backoff]
        # SQLAlchemy automatically uses delays between failed connection attempts,
        # but provides no arguments for configuration.
        # [END cloud_sql_mysql_sqlalchemy_backoff]
        # [START cloud_sql_mysql_sqlalchemy_timeout]
        # 'pool_timeout' is the maximum number of seconds to wait when retrieving a
        # new connection from the pool. After the specified amount of time, an
        # exception will be thrown.
        pool_timeout=30,  # 30 seconds
        # [END cloud_sql_mysql_sqlalchemy_timeout]
        # [START cloud_sql_mysql_sqlalchemy_lifetime]
        # 'pool_recycle' is the maximum number of seconds a connection can persist.
        # Connections that live longer than the specified amount of time will be
        # reestablished
        pool_recycle=1800,  # 30 minutes
        # [END cloud_sql_mysql_sqlalchemy_lifetime]
        # [END_EXCLUDE]
    )
    # [END cloud_sql_mysql_sqlalchemy_create]

  def get_airport_by_iata(self, iata_code):
    """Given an IATA code, look up that airport's name.

    Args:
      iata_code: (string) The IATA code of the airport to find.

    Returns:
      string: The airport name, if found.
      None: The airport was not found.
    """

    with self.db.connect() as conn:
      stmt = sqlalchemy.text(
              "SELECT name FROM airports WHERE iata_code=:iata_code"
          )

      airport_name_result = conn.execute(stmt, iata_code=iata_code).fetchone()

      if airport_name_result:
        airport_name = airport_name_result[0]
        return airport_name
    
    return None

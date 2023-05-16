# RottenTomato Movie Detail Scrapping with python RPAFramework

This is the object oriented part for the previous [procedure part](https://github.com/Saurab-Shrestha/rottentomato-automation).

## Process
1. Opens rottentomatoes.com
2. Searches each movie in the provided excel file. (only movies should be searched, not tv shows etc.)
3. Search for exact matches only.(case insensitive) e.g. if the provided movie is Titanic, then Titanic 666 is not a match.
4. If multiple exact matches are found, take the movie that was released most recently by year.
5. Extract TOMATOMETER score, AUDIENCE SCORE, storyline, rating, genres and top 5 critic reviews. The data should be saved to sqlite database
6. Sqlite database should be created on the first run with following columns. On subsequent runs, data is inserted only id, movie_name, tomatometer_score, audience_score, storyline, rating, genres, review_1, review_2, review_3, review_4, review_5, status
7. If no exact match is found in search, insert ‘No exact match found’ in the status field otherwise success in statu

## RPAFramework

This is the simplest template to start from.

- Get started from a simple task template in `tasks.robot`.
  - Uses [Robot Framework](https://robocorp.com/docs/languages-and-frameworks/robot-framework/basics) syntax.
- You can configure your robot `robot.yaml`.
- You can configure dependencies in `conda.yaml`.

## Learning materials

- [Robocorp Developer Training Courses](https://robocorp.com/docs/courses)
- [Documentation links on Robot Framework](https://robocorp.com/docs/languages-and-frameworks/robot-framework)
- [Example bots in Robocorp Portal](https://robocorp.com/portal)

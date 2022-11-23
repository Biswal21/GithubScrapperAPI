## System Design

### Assumption

- The hiring team members will feed in the:
    - Keywords (can be multiple)
    - Location of user required
    - Programming Languages user should have worked on
    - Sort the list (Optional)
- So our server should able to process all the conditions or filters provided from theb frontend side to the server and then use ******Github Search API****** to find users accordingly as query params for the API.


## Architecture

![App Screenshot](https://imgur.com/a/hNUK7Br)

### Design Ideology

- As soon as the query filters are received by the server, the server should start fetching user’s information from github API and and then process them according to the required schema of **CSV format.**
- Along with that the processed data is stored in a relational database, postgres database in specific has been used in this project.
## API Reference

#### The Keyword filter schema is →


```http
  POST /main/user/fetch/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `query_keyword` | [`string`] | **Required**.Filter Keywords  |
| `location` | `string` |  Users from location |
| `language` | [`string`] |  List of programming languages used |
| `sort` | `string` |  Options: `joined`, `repositories`, `followers` |

#### Get Github Users data 

```http
  GET /main/user/read/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `int` |  Id of user data |
| `name`      | `string` |  Name of user |
| `github_handle`      | `string` |  Github handle of user |
| `blurb`      | `string` |  Bio of user  |
| `location`      | `string` |  Location of user  |
| `github_profile_link`      | `url` |  Github profile link of user  |
| `twitter_handle`      | `string` |  Twitter handle of user  |
| `email`      | `string` |  Email of user  |
| `created_at`      | `datetime` |  User data created  |
| `updated_at`      | `datetime` |  User data updated  |


### Features Not Implemented

- Other contacting links in user's data
- User contribution graph



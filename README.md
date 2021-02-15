# 🪐PLAN:NET

👩‍👧‍👧 신뢰도가 보장된 팀원과 함께하는 온라인 스터디 플랫폼



## 사용 기술

Language: Python

Framework: Flask

NoSQL Database: Cassandra



## 기능 명세

### 로그인

Google OAuth

최초 로그인 시 관심있는 카테고리를 선택한다.



#### 스터디룸 - 모집 중

생성: Danbee.ai를 활용해 만든 챗봇을 통해 스터디를 생성한다. 스터디를 생성한 유저는 자동적으로 방장 권한을 갖게 된다.

추천: 모집중인 스터디를 유저가 관심있는 카테고리에 따라 노출한다. 노출되는 순서는 매일 현재 스터디에 가입한 팀원들의 경험치를 기반으로 환산한 점수에 따라 달라진다.

가입: 추천 목록에 노출되는 스터디에 대한 기본적인 정보를 확인한 후, 스터디에 가입한다.

모집 마감: 방장이 모집을 마감하면, 스터디는 진행 중 상태로 전환된다.



#### 스터디룸 - 진행 중

meets: 구글 meets를 생성하여 스터디를 진행하고, 각자의 진행상황을 확인할 수 있다.

진척도: 방장은 현재 팀원들의 상황을 확인한 뒤, 스터디 전체의 진척도를 설정할 수 있다. 진척도가 100% 채워지면 방장은 스터디를 완료 상태로 전환할 수 있다.

TODO: 방장을 포함한 모든 팀원은 각자의 할 일을 추가할 수 있고, 완료된 할 일에 대해 상태를 전환할 수 있다.

페널티: 팀원의 출결 등을 토대로 페널티를 부과한다. 부과된 페널티가 스터디 생성 시 설정한 최대 페널티 점수에 다다르면 해당 팀원은 강제로 스터디에서 퇴출된다.

랭킹: 매일 팀의 진척도와 방장을 포함한 모든 팀원의 출석률, TODO 진행 상황을 기반으로 점수를 환산하여 모든 스터디룸의 랭킹을 매긴다.



#### 스터디룸 - 완료

업적: 방장을 포함한 팀원들의 업적 정보를 업데이트한다.

경험치: 방장을 포함한 팀원들의 경험치를 업데이트한다.
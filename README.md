<h1 align="center">🪐PLAN:NET</h1>
<p>
</p>
<div align="center">
<img src="https://img.shields.io/badge/Python-3766AB?style=flat-square&logo=Python&logoColor=white" class="center"/></a>&nbsp;
<img src="https://img.shields.io/badge/Flask-000000?style=flat-square&logo=Flask" class="center"/></a>&nbsp;
<img  src="https://img.shields.io/badge/Apache_Cassandra-1287B1?style=flat-square&logo=Apache%20Cassandra&logoColor=white" class="center"/></a>&nbsp;
</div>
<p>
</p>
<div>&nbsp;</div>

  


> 👩‍👧‍👧 신뢰도가 보장된 팀원과 함께하는 온라인 스터디 플랫폼
<div>&nbsp;</div>
  

## 구현 목표

코로나19로 인해 비대면 스터디가 활성화되고 있다. 하지만 팀원의 문제로 스터디의 목표를 달성하지 못하고 해산하는 경우가 많이 발생한다.

이러한 문제점을 인지하고, 신뢰도가 보장된 팀원을 구해 꾸준히 스터디를 지속할 수 있도록 하여 목표 달성을 돕는 시스템을 구현하고자 한다.  
<div>&nbsp;</div>
  

  

## 주요 기능

### 로그인

로그인은 Google OAuth를 통해 가능하다. 최초 로그인 시, 관심있는 카테고리를 다수 선택할 수 있다.
  

### 스터디 추천

아직 어떤 스터디에도 참여하지 않은 유저에게 스터디를 추천한다.

유저가 선택한 관심 카테고리를 기반으로 추천될 스터디들이 결정되며, 노출되는 순서는 해당 스터디에 참여하고 있는 유저들의 경험치 등을 기반으로 정해진다.

  


### 스터디 생성 및 가입

스터디는 Danbee.ai를 활용해 만든 챗봇을 통해 생성할 수 있으며, 스터디를 생성한 유저는 자동적으로 방장 권한을 갖게 된다. 

그 외 유저들은 추천받은 스터디 중 스터디를 선택해 참여할 수 있다.

방장은 참여한 스터디원의 수가 충분하다고 판단하면 해당 스터디를 시작할 수 있다.

  

### 스터디 진행

스터디원들은 각자의 할 일을 추가, 완료하여 달성률을 올릴 수 있으며, 다른 스터디원의 달성률 또한 확인 가능하다.

로그인한 구글 아이디를 통해 구글 meets를 생성하여 다른 스터디원과 함께 스터디를 진행할 수 있으며, 스터디마다 스터디원들의 출석률을 체크한다.

스터디원의 출결이나 달성률 등을 토대로 페널티가 부과된다. 부과된 페널티가 스터디의 최대 페널티에 다다르면 해당 팀원은 스터디에서 강제 퇴출된다.

  

### 스터디 완료

스터디의 달성률이 100에 도달하면, 방장에게는 스터디를 종료할 수 있는 권한이 주어진다. 방장이 스터디를 종료하게 되면, 모든 스터디원은 다른 스터디원들의 평가를 할 수 있는 페이지에 접근할 수 있다.

각 스터디원의 평가와 할 일 달성률, 출결 등을 기반으로 경험치와 업적 정보를 업데이트된다.

  

### 랭킹

각 스터디의 달성률, 스터디원의 할 일 달성률, 출결률 등을 반영하여 매일 모든 스터디 혹은 각 카테고리마다 스터디의 랭킹을 산출한다.

각 유저의 경험치, 업적 등을 반영하여 매일 모든 유저의 랭킹을 산출한다.
<div>&nbsp;</div>

  

  

## Requirements

```
cassandra-driver==3.4.0
cql==1.4.0
Flask==1.1.2
Flask-Login==0.5.0
oauthlib==3.1.0
pyOpenSSL @ file:///tmp/build/80754af9/pyopenssl_1594392929924/work
requests @ file:///tmp/build/80754af9/requests_1592841827918/work
```
<div>&nbsp;</div>

  

  

## Contributors

<table style="border-collapse: collapse; border: none;" bgcolor="ffffff">
  <tr style="border: none;" align="center">
    <td style="border: none;" align="center"><a href="https://github.com/kyueun"><img src="https://avatars.githubusercontent.com/u/29202047?v=4" width="100px;" alt=""/><br /><sub><b>kyueun</b></sub></a><br /><a href="https://github.com/orgs/cosmic-plannet/people/kyueun" title="Code">🗃 👩‍💻</a></td>
    <td style="border: none;" align="center"><a href="https://github.com/JHC21"><img src="https://avatars.githubusercontent.com/u/57344372?v=4" width="100px;" alt=""/><br /><sub><b>JHC21</b></sub></a><br /><a href="https://github.com/orgs/cosmic-plannet/people/JHC21" title="Code">💬 👩‍💻</a></td>
  </tr>
</table>
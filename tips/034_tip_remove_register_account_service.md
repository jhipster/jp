---
layout: default
title: アカウント登録サービスを削除する
sitemap:
priority: 0.1
lastmod: 2021-03-19T21:22:00-00:00
---
# アカウント登録サービスを削除する

__このTipは[@apuntandoanulo](https://github.com/apuntandoanulo)により提出されました__

_目標:_ ユーザーがアカウントを作成できる可能性を排除し、以前に登録したユーザーのみだけにそれをさせたい場合は、次に示すコードの一部と行を削除します。

## 1.バックエンド側

* ___1.1___  src\main\java\ ... \service\UserService.java
  - メソッド全体を削除します：`public User registerUser(...)`
* ___1.2___ src\main\java\ ... \rest\AccountResource.java
  - メソッド全体を削除します：`@PostMapping("/register")   public void registerAccount(...)`

## 2.フロントエンド側

* ___2.1___ src\main\webapp\app\account\
  - 次の内容を含むフォルダ`register`全体を削除します：`register.component.html`、`register.component.ts`、`register.route.ts`、`register.service.ts`

* ___2.2___ `src\main\webapp\app\account\account.module.ts`に移動して、次の行を削除します。
  - ``` import { RegisterComponent } from './register/register.component'; ```
  - _declarations_ array -> ```  RegisterComponent, ```

* ___2.3___ `src\main\webapp\app\account\account.route.ts`に移動して、次の行を削除します。
  - ``` import { registerRoute } from './register/register.route'; ```
  - _ACCOUNT_ROUTES_ array -> ```  registerRoute ```

* ___2.4___ `src\main\webapp\app\home\home.component.html`に移動し、次のブロックを削除します。
  ```
  <div class="alert alert-warning" *ngSwitchCase="false">
    <span jhiTranslate="global.messages.info.register.noaccount">You don't have an account yet?</span>&nbsp;
    <a class="alert-link" routerLink="account/register" jhiTranslate="global.messages.info.register.link">Register a new account</a>
  </div>
  ```

* ___2.5___ `src\main\webapp\app\layouts\navbar\navbar.component.html`に移動して、次のブロックを削除します。
  ```
  <li *ngSwitchCase="false">
    <a class="dropdown-item" routerLink="account/register" routerLinkActive="active" (click)="collapseNavbar()">
        <fa-icon icon="user-plus" [fixedWidth]="true"></fa-icon>
        <span jhiTranslate="global.menu.account.register">Register</span>
    </a>
  </li>
  ```

* ___2.6___ `src\main\webapp\app\shared\login\login.component.html`に移動し、次のブロックを削除します。
  ```
  <div class="alert alert-warning">
    <span jhiTranslate="global.messages.info.register.noaccount">You don't have an account yet?</span>
    <a class="alert-link" (click)="register()" jhiTranslate="global.messages.info.register.link">Register a new account</a>
  </div>
  ```

* ___2.7___ `src\main\webapp\app\shared\login\login.component.ts`に移動し、次のブロックを削除します。
  ```
  register(): void {
    this.activeModal.dismiss('to state register');
    this.router.navigate(['/account/register']);
  }
  ```

* ___2.8___ メッセージ・ファイルを削除します：``` src\main\webapp\i18n\ ... \register.json ```

* ___2.9___ src\test\javascript\spec\app\account
  - 次の内容を含むフォルダ`register`全体を削除します：`register.component.spec.ts`

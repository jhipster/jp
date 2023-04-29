---
layout: default
title: LDAP認証
sitemap:
priority: 0.5
lastmod: 2019-11-11T22:22:00-00:00
---

# LDAP認証

__このTipは[@mleneveut](https://github.com/mleneveut)により提出され__  [@patrickjp93](https://github.com/patrickjp93)により更新されました。

JHipsterアプリケーションにLDAP認証を追加するには、次の手順に従います。

  * spring-ldap-coreとspring-security-ldapの依存関係を追加します。gradleでのbuild.gradleの例です。

```
    compile group: 'org.springframework.security', name: 'spring-security-ldap', version: spring_security_version
```
  * SecurityConfiguration.javaを変更し、メソッドconfigureGlobal(AuthenticationManagerBuilder auth)とgetContextSource()を追加します。
  * 次のクエリ文字列は、理想的には[環境変数にカプセル化する](https://github.com/eugenp/tutorials/blob/master/spring-ldap/src/main/java/com/baeldung/ldap/javaconfig/AppConfig.java)か、少なくともproperties/ymlファイルにカプセル化する必要があります。 

```
    @Inject
    public void configureGlobal(AuthenticationManagerBuilder auth) throws Exception {
        auth.ldapAuthentication()
        	.userSearchBase("o=myO,ou=myOu") //ベースを追加しない
        	.userSearchFilter("(uid={0})")
        	.groupSearchBase("ou=Groups") //ベースを追加しない
        	.groupSearchFilter("member={0}")
        	.contextSource(getContextSource());
    }
    @Bean
    public LdapContextSource getContextSource() {
    	  LdapContextSource contextSource = new LdapContextSource();
        contextSource.setUrl("ldap://[IP goes here]:[port goes here]");
        contextSource.setBase("dc=mycompany,dc=com");
        contextSource.setUserDn("cn=aUserUid,dc=mycompany,dc=com");
        contextSource.setPassword("hisPassword");
        contextSource.afterPropertiesSet(); //必要です。さもなければSpringでNullPointerExceptionが発生します。

        return contextSource;
    }

```
  * SecurityUtils.javaのメソッドgetCurrentUserLogin()を変更します。

```
    } else if (authentication.getPrincipal() instanceof LdapUserDetails) {
    	LdapUserDetails ldapUser = (LdapUserDetails) authentication.getPrincipal();
    	return ldapUser.getUsername();
    }
```
  * 新しいCustomAuthenticationManagerクラスを追加します。AuthenticationManagerインタフェースを実装し、認証方式をオーバーライドして、認証プロセスがLDAPを介してユーザーを認証を強制するようにします。

```

@Component
public class CustomAuthenticationManager implements AuthenticationManager {

    LdapAuthenticationProvider provider = null;

    private static final Logger log = LoggerFactory.getLogger(CustomAuthenticationManager.class);

    private final UserRepository userRepository;

    @Autowired
    private final LdapContextSource ldapContextSource;

    public CustomAuthenticationManager(UserRepository userRepository, LdapContextSource ldapContextSource) {
        this.userRepository = userRepository;
        this.ldapContextSource = ldapContextSource;
    }

    @Override
    public Authentication authenticate(Authentication authentication) {
        log.debug("AUTHENTICATION Login" + authentication.getName());
        log.debug("AUTHENTICATION Password" + authentication.getCredentials().toString());

        BindAuthenticator bindAuth = new BindAuthenticator(ldapContextSource);
        FilterBasedLdapUserSearch userSearch = new FilterBasedLdapUserSearch(
                "", "(uid={0})",
                ldapContextSource);
        try{
            bindAuth.setUserSearch(userSearch);
            bindAuth.afterPropertiesSet();
        } catch (Exception ex) {
            java.util.logging.Logger.getLogger(CustomAuthenticationManager.class.getName()).log(Level.SEVERE, null, ex);
        }
        provider = new LdapAuthenticationProvider(bindAuth);
        provider.setUserDetailsContextMapper(new UserDetailsContextMapper() {
            @Override
            public UserDetails mapUserFromContext(DirContextOperations ctx, String username, Collection<? extends GrantedAuthority> clctn) {
                Optional<User> isUser = userRepository.findOneWithAuthoritiesByLogin(username);
                final User user = isUser.get();
                Set<Authority> userAuthorities = user.getAuthorities();
                Collection<GrantedAuthority> grantedAuthorities = new ArrayList<>();
                for(Authority a: userAuthorities){
                    GrantedAuthority grantedAuthority = new SimpleGrantedAuthority(
                            a.getName());
                    grantedAuthorities.add(grantedAuthority);
                }
                  return new org.springframework.security.core.userdetails.User(
                    username, "1" , grantedAuthorities);    
            }

            @Override
            public void mapUserToContext(UserDetails ud, DirContextAdapter dca) {

            }
        });
        return provider.authenticate(authentication);
    }

```

  * 一部のLDAPサーバでは、次の認証実装の方が成功していますが、ユーザ認証されたユーザをユーザテーブルにマッピングし、ADグループに基づいて権限を設定するには、より多くの作業が必要です。
  * [@eugenp](https://github.com/eugenp/tutorials/tree/master/spring-ldap)と[Michael Kostewicz](http://code-addict.pl/active-directory-spring-security/)の安定したリファレンス実装に感謝します。
```  
  public Authentication authenticate(Authentication authentication) {
        log.info("Authorizing active directory ldap ....");
        
        Hashtable<String, String> ldapEnv = new Hashtable<>(Map.of(
            Context.INITIAL_CONTEXT_FACTORY, this.InitialContextFactory,
            Context.PROVIDER_URL, this.ProviderUrl,
            Context.SECURITY_AUTHENTICATION, this.SecurityAuthentication,
            Context.SECURITY_PRINCIPAL, this.UserDomain + authentication.getPrincipal(),
            Context.SECURITY_CREDENTIALS, authentication.getCredentials().toString(),
            Context.SECURITY_PROTOCOL, "ssl"
        ));

        try {
            ldapContext = new InitialDirContext(ldapEnv);
            authentication.setAuthenticated(true);
            log.info("Connected and authenticated.");
            ldapContext.close();
        } catch (Exception e) { 
            log.error(e.getMessage()); 
        }
        return authentication;
    }
```

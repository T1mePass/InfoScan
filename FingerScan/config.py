import random
import re
import sqlite3
import os

cms_finger_list = ['08cms', '1039_jxt', '1039\xe5\xae\xb6\xe6\xa0\xa1\xe9\x80\x9a', '3gmeeting',
                   '3gmeeting\xe8\xa7\x86\xe8\xae\xaf\xe7\xb3\xbb\xe7\xbb\x9f',
                   '51fax\xe4\xbc\xa0\xe7\x9c\x9f\xe7\xb3\xbb\xe7\xbb\x9f', '53kf', '5ucms', '686_weixin', '6kbbs',
                   '74cms', '86cms', 'afterlogicwebmail\xe7\xb3\xbb\xe7\xbb\x9f', 'appcms', 'aspcms', 'b2bbuilder',
                   'beescms', 'bookingecms\xe9\x85\x92\xe5\xba\x97\xe7\xb3\xbb\xe7\xbb\x9f',
                   'cactiez\xe6\x8f\x92\xe4\xbb\xb6', 'chinacreator', 'cxcms', 'dk\xe5\x8a\xa8\xe7\xa7\x91cms',
                   'doyo\xe9\x80\x9a\xe7\x94\xa8\xe5\xbb\xba\xe7\xab\x99\xe7\xb3\xbb\xe7\xbb\x9f', 'dtcms',
                   'dvrdvs-webs', 'datalifeengine', 'dayucms', 'dedecms', 'destoon', 'digital campus2.0',
                   'digitalcampus2.0', 'discuz', 'discuz7.2', 'drupal', 'dswjcms', 'duomicms', 'dvbbs', 'dzzoffice',
                   'ecshop', 'ec_word\xe4\xbc\x81\xe4\xb8\x9a\xe7\xae\xa1\xe7\x90\x86\xe7\xb3\xbb\xe7\xbb\x9f', 'emlog',
                   'easysite\xe5\x86\x85\xe5\xae\xb9\xe7\xae\xa1\xe7\x90\x86', 'edusoho', 'empirecms',
                   'epaper\xe6\x8a\xa5\xe5\x88\x8a\xe7\xb3\xbb\xe7\xbb\x9f', 'epoint', 'espcms', 'fengcms', 'foosuncms',
                   'gentlecms', 'gever', 'glassfish',
                   'h5\xe9\x85\x92\xe5\xba\x97\xe7\xae\xa1\xe7\x90\x86\xe7\xb3\xbb\xe7\xbb\x9f', 'hdwiki',
                   'hjcms\xe4\xbc\x81\xe4\xb8\x9a\xe7\xbd\x91\xe7\xab\x99\xe7\xae\xa1\xe7\x90\x86\xe7\xb3\xbb\xe7\xbb\x9f',
                   'himail', 'hishop\xe5\x95\x86\xe5\x9f\x8e\xe7\xb3\xbb\xe7\xbb\x9f', 'hituxcms',
                   'ilas\xe5\x9b\xbe\xe4\xb9\xa6\xe7\xb3\xbb\xe7\xbb\x9f',
                   'iloanp2p\xe5\x80\x9f\xe8\xb4\xb7\xe7\xb3\xbb\xe7\xbb\x9f',
                   'imo\xe4\xba\x91\xe5\x8a\x9e\xe5\x85\xac\xe5\xae\xa4\xe7\xb3\xbb\xe7\xbb\x9f', 'insightsoft',
                   'iwebshop', 'iwmscms', 'jboos', 'jishigou', 'jeecms', 'jingyi', 'joomla',
                   'kangle\xe8\x99\x9a\xe6\x8b\x9f\xe4\xb8\xbb\xe6\x9c\xba', 'kesioncms', 'kessioncms', 'kingcms',
                   'lebishop\xe7\xbd\x91\xe4\xb8\x8a\xe5\x95\x86\xe5\x9f\x8e', 'live800',
                   'live800\xe6\x8f\x92\xe4\xbb\xb6', 'ljcms', 'mlecms', 'mailgard', 'majexpress', 'mallbuilder',
                   'maticsoftsns', 'minyoocms', 'mvmmall',
                   'mymps\xe8\x9a\x82\xe8\x9a\x81\xe5\x88\x86\xe7\xb1\xbb\xe4\xbf\xa1\xe6\x81\xaf',
                   'n\xe7\x82\xb9\xe8\x99\x9a\xe6\x8b\x9f\xe4\xb8\xbb\xe6\x9c\xba', 'opensns', 'ourphp', 'php168',
                   'phpcms', 'phpwind', 'phpok',
                   'piw\xe5\x86\x85\xe5\xae\xb9\xe7\xae\xa1\xe7\x90\x86\xe7\xb3\xbb\xe7\xbb\x9f', 'phpmyadmin',
                   'phpwind\xe7\xbd\x91\xe7\xab\x99\xe7\xa8\x8b\xe5\xba\x8f', 'pigcms',
                   'powercreator\xe5\x9c\xa8\xe7\xba\xbf\xe6\x95\x99\xe5\xad\xa6\xe7\xb3\xbb\xe7\xbb\x9f', 'powereasy',
                   'sapnetweaver', 'shopex', 'shop7z', 'shopnc\xe5\x95\x86\xe5\x9f\x8e\xe7\xb3\xbb\xe7\xbb\x9f',
                   'shopnum', 'siteserver', 'soullon', 'southidc', 'supesite',
                   't-site\xe5\xbb\xba\xe7\xab\x99\xe7\xb3\xbb\xe7\xbb\x9f',
                   'theol\xe7\xbd\x91\xe7\xbb\x9c\xe6\x95\x99\xe5\xad\xa6\xe7\xbb\xbc\xe5\x90\x88\xe5\xb9\xb3\xe5\x8f\xb0',
                   'trs\xe8\xba\xab\xe4\xbb\xbd\xe8\xae\xa4\xe8\xaf\x81\xe7\xb3\xbb\xe7\xbb\x9f',
                   'tipask\xe9\x97\xae\xe7\xad\x94\xe7\xb3\xbb\xe7\xbb\x9f', 'tomcat', 'trsids', 'trunkey',
                   'turbomail\xe9\x82\xae\xe7\xae\xb1\xe7\xb3\xbb\xe7\xbb\x9f',
                   'v2\xe8\xa7\x86\xe9\xa2\x91\xe4\xbc\x9a\xe8\xae\xae\xe7\xb3\xbb\xe7\xbb\x9f', 'v5shop',
                   'venshop2010\xe5\x87\xa1\xe4\xba\xba\xe7\xbd\x91\xe7\xbb\x9c\xe8\xb4\xad\xe7\x89\xa9\xe7\xb3\xbb\xe7\xbb\x9f',
                   'vos3000', 'veryide', 'wcm\xe7\xb3\xbb\xe7\xbb\x9fv6', 'wordpress',
                   'ws2004\xe6\xa0\xa1\xe5\x9b\xad\xe7\xae\xa1\xe7\x90\x86\xe7\xb3\xbb\xe7\xbb\x9f', 'wangzt',
                   'weblogic', 'webmail', 'weboffice', 'webnet cms', 'webnetcms', 'wilmaroa\xe7\xb3\xbb\xe7\xbb\x9f',
                   'winmail server', 'winmailserver', 'wizbank',
                   'xplus\xe6\x8a\xa5\xe7\xa4\xbe\xe7\xb3\xbb\xe7\xbb\x9f', 'xpshop', 'yidacms', 'yongyou', 'z-blog',
                   'zabbix', 'zoomla', 'abcms', 'able_g2s', 'acsno', 'acsoft', 'actcms', 'adtsec_gateway', 'akcms',
                   'anleye', 'anmai',
                   'anmai\xe5\xae\x89\xe8\x84\x89\xe6\x95\x99\xe5\x8a\xa1\xe7\xae\xa1\xe7\x90\x86\xe7\xb3\xbb\xe7\xbb\x9f',
                   'anymacromail', 'apabi_tasi', 'asiastar_sm', 'aten_kvm', 'atripower', 'avcon6', 'axis2', 'ayacms',
                   'b2cgroup', 'baiaozhi', 'beidou', 'bluecms', 'boblog', 'bocweb', 'bohoog', 'bytevalue_router',
                   'canon', 'chamilo-lms', 'ckfinder', 'cmseasy', 'cmstop', 'cnoa', 'codeigniter', 'comexe_ras',
                   'cscms', 'cutecms', 'd-link', 'dahua_dss', 'daiqile_p2p', 'dalianqianhao', 'damall', 'damicms',
                   'dfe_scada', 'dianyips', 'diguocms\xe5\xb8\x9d\xe5\x9b\xbd', 'dircms', 'dkcms', 'dossm', 'douphp',
                   'dreamgallery', 'dubbo', 'eshangbao\xe6\x98\x93\xe5\x95\x86\xe5\xae\x9d', 'easethink',
                   'easy7\xe8\xa7\x86\xe9\xa2\x91\xe7\x9b\x91\xe6\x8e\xa7\xe5\xb9\xb3\xe5\x8f\xb0', 'ecweb_shop',
                   'edayshop', 'edjoy', 'eduplate', 'edusohocms', 'eims', 'eimscms', 'electric_monitor', 'empire_cms',
                   'enableq', 'enjie_soft', 'es-cloud', 'esafenet_dlp', 'esccms', 'ewebs', 'expocms', 'extmail', 'eyou',
                   'e\xe5\x88\x9b\xe7\xab\x99', 'fang5173', 'fangwei', 'fastmeeting', 'fcms',
                   'fcms\xe6\xa2\xa6\xe6\x83\xb3\xe5\xbb\xba\xe7\xab\x99', 'feifeicms', 'feiyuxing_router', 'finecms',
                   'fiyocms', 'foosun', 'foosun\xe6\x96\x87\xe7\xab\xa0\xe7\xb3\xbb\xe7\xbb\x9f', 'fsmcms',
                   'gbcom_wlan', 'genixcms', 'gnuboard', 'gocdkey', 'gooine_sqjz', 'gowinsoft_jw', 'gxcms',
                   'hac_gateway', 'haitianoa', 'hanweb', 'haohan', 'heeroa', 'hf_firewall', 'hongzhi', 'horde_email',
                   'house5', 'hsort', 'huachuang_router', 'huanet', 'huashi_tv', 'humhub', 'idvr', 'ipowercms',
                   'iceflow_vpn_router', 'ideacms', 'ieadcms', 'iflytek_soft', 'igenus', 'ikuai', 'insight', 'jenkins',
                   'jienuohan', 'jieqicms', 'jindun_gateway', 'jingci_printer', 'jinpan', 'jinqiangui_p2p',
                   'jishitongxun', 'joomle', 'jumbotcms', 'juniper_vpn', 'kill_firewall', 'kingdee_eas', 'kingdee_oa',
                   'kinggate', 'kingosoft_xsweb', 'kj65n_monitor', 'klemanndesign', 'kuwebs', 'kxmail', 'landray',
                   'lebishop', 'lezhixing_datacenter', 'lianbangsoft', 'liangjing', 'libsys', 'linksys', 'looyu_live',
                   'ltpower', 'luepacific', 'luzhucms', 'lvmaque', 'maccms', 'magento', 'mailgard-webmail',
                   'mainone_b2b', 'maopoa', 'maxcms', 'mbbcms', 'metinfo', 'mikrotik_router', 'moxa_nport_router',
                   'mpsec', 'myweb', 'nanjing_shiyou', 'natshell', 'nbcms', 'net110', 'netcore', 'netgather',
                   'netoray_nsg', 'netpower', 'newvane_onlineexam', 'nitc',
                   'nitc\xe5\xae\x9a\xe6\xb5\xb7\xe7\xa5\x9e\xe7\x9c\x9f', 'niubicms', 'ns-asg', 'otcms', 'pageadmin',
                   'panabit', 'phpb2b', 'phpcmsv9', 'phpdisk', 'phpmaps', 'phpmps', 'phpmywind', 'phpshe', 'phpshop',
                   'phpvibe', 'phpweb', 'phpwiki', 'phpyun', 'piaoyou', 'pkpmbs', 'plc_router', 'powercreator',
                   'qht_study', 'qianbocms', 'qibosoft', 'qiuxue', 'qizhitong_manager',
                   'qzdatasoft\xe5\xbc\xba\xe6\x99\xba\xe6\x95\x99\xe5\x8a\xa1\xe7\xae\xa1\xe7\x90\x86\xe7\xb3\xbb\xe7\xbb\x9f',
                   'rockoa', 'rockontrol', 'ruijie_router', 'ruvar_oa', 'ruvarhrm', 's8000', 'santang', 'sdcms',
                   'seagate_nas', 'seawind', 'seentech_uccenter', 'sgc8000', 'shadows-it', 'shenlan_jiandu', 'shlcms',
                   'shopnum1', 'shopxp', 'shuangyang_oa', 'siteengine', 'sitefactory', 'skypost', 'skytech', 'smart_oa',
                   'soffice', 'soullon_edu', 'srun_gateway', 'star-net', 'startbbs', 'strongsoft', 'subeicms',
                   'syncthru_web_service', 'synjones_school', 'syxxjs', 'sztaiji_zw', 'taocms', 'taodi', 'terramaster',
                   'thinkox', 'thinkphp', 'thinksns', 'tianbo_train', 'tianrui_lib', 'tipask', 'tongdaoa', 'topsec',
                   'totalsoft_lib', 'tp-link', 'trs_ids', 'trs_inforadar', 'trs_lunwen', 'trs_wcm', 'typecho', 'umail',
                   'uniflows', 'unis_gateway', 'uniwin_gov', 'urp', 'v2_conference', 'vbulletin', 'vicworl',
                   'visionsoft_velcro', 'wangqushop', 'wdcp', 'wdscms', 'weaver_oa', 'websitebaker', 'wecenter',
                   'weixinpl', 'weway_soft', 'wisedu_elcs', 'workyisystem', 'workyi_system', 'wygxcms', 'xdcms',
                   'xiaowuyou_cms', 'xikecms', 'xinhaisoft', 'xinyang', 'xinzuobiao', 'xplus', 'xr_gatewayplatform',
                   'xuezi_ceping', 'xycms', 'ynedut_campus', 'yongyou_a8', 'yongyou_crm', 'yongyou_ehr', 'yongyou_fe',
                   'yongyou_icc', 'yongyou_nc', 'yongyou_u8', 'yongyou_zhiyuan_a6', 'yuanwei_gateway', 'yxlink',
                   'zblog', 'zcncms', 'zdsoft_cnet', 'zentao', 'zeroboard', 'zf_cms', 'zfsoft', 'zhongdongli_school',
                   'zhonghaida_vnet', 'zhongqidonglicms', 'zhongruan_firewall', 'zhoupu', 'zhuangxiu',
                   'zhuhaigaoling_huanjingzaosheng', 'zmcms', 'zmcms\xe5\xbb\xba\xe7\xab\x99', 'zte', 'zuitu', 'zzcms',
                   '\xe4\xb8\x87\xe4\xbc\x97\xe7\x94\xb5\xe5\xad\x90\xe6\x9c\x9f\xe5\x88\x8acms',
                   '\xe4\xb8\x87\xe5\x8d\x9a\xe7\xbd\x91\xe7\xab\x99\xe7\xae\xa1\xe7\x90\x86\xe7\xb3\xbb\xe7\xbb\x9f2006',
                   '\xe4\xb8\x87\xe5\x8d\x9a\xe7\xbd\x91\xe7\xab\x99\xe7\xae\xa1\xe7\x90\x86\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe4\xb8\x87\xe6\x88\xb7oa',
                   '\xe4\xb8\x87\xe6\xac\xa3\xe9\xab\x98\xe6\xa0\xa1\xe7\xae\xa1\xe7\x90\x86\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe4\xb8\x89\xe6\x89\x8d\xe6\x9c\x9f\xe5\x88\x8a\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe4\xb8\xad\xe4\xbc\x81\xe5\x8a\xa8\xe5\x8a\x9bcms',
                   '\xe4\xb9\x90\xe5\xbd\xbc\xe5\xa4\x9a\xe7\xbd\x91\xe5\xba\x97', '\xe4\xba\xbf\xe9\x82\xaeemail',
                   '\xe4\xbc\x81\xe6\x99\xba\xe9\x80\x9a\xe7\xb3\xbb\xe5\x88\x97\xe4\xb8\x8a\xe7\xbd\x91\xe8\xa1\x8c\xe4\xb8\xba\xe7\xae\xa1\xe7\x90\x86\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe4\xbc\x97\xe6\x8b\x93', '\xe5\x85\xa8\xe7\xa8\x8boa',
                   '\xe5\x87\xa1\xe8\xaf\xba\xe4\xbc\x81\xe4\xb8\x9a\xe7\xbd\x91\xe7\xab\x99\xe7\xae\xa1\xe7\x90\x86\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe5\x88\x86\xe7\xb1\xbb\xe4\xbf\xa1\xe6\x81\xaf\xe7\xbd\x91bank.asp\xe5\x90\x8e\xe9\x97\xa8',
                   '\xe5\x88\x9b\xe6\x8d\xb7\xe9\xa9\xbe\xe6\xa0\xa1\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe5\x8d\x8e\xe5\xa4\x8f\xe5\x88\x9b\xe6\x96\xb0appex\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe5\x8d\x97\xe6\x96\xb9\xe6\x95\xb0\xe6\x8d\xae',
                   '\xe5\x8f\xa3\xe7\xa6\x8f\xe7\xa7\x91\xe6\x8a\x80',
                   '\xe5\x91\xb3\xe5\xa4\x9a\xe7\xbe\x8e\xe5\xaf\xbc\xe8\x88\xaa', '\xe5\x95\x86\xe5\xa5\x87cms',
                   '\xe5\x95\x86\xe5\xae\xb6\xe4\xbf\xa1\xe6\x81\xaf\xe7\xae\xa1\xe7\x90\x86\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe5\x9b\x9b\xe9\x80\x9a\xe6\x94\xbf\xe5\xba\x9c\xe7\xbd\x91\xe7\xab\x99\xe7\xae\xa1\xe7\x90\x86\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe5\xa4\xa7\xe6\xb1\x89jcms',
                   '\xe5\xa4\xa9\xe6\x9f\x8f\xe5\x9c\xa8\xe7\xba\xbf\xe8\x80\x83\xe8\xaf\x95\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe5\xa4\xa9\xe8\x9e\x8d\xe4\xbf\xa1panabit',
                   '\xe5\xae\x81\xe5\xbf\x97\xe5\xad\xa6\xe6\xa0\xa1\xe7\xbd\x91\xe7\xab\x99',
                   '\xe5\xae\x81\xe5\xbf\x97\xe5\xad\xa6\xe6\xa0\xa1\xe7\xbd\x91\xe7\xab\x99\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe5\xae\x89\xe4\xb9\x90\xe4\xb8\x9a\xe6\x88\xbf\xe4\xba\xa7\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe5\xae\x9a\xe6\xb5\xb7\xe7\xa5\x9e\xe7\x9c\x9f',
                   '\xe5\xb0\x8f\xe8\xae\xa1\xe5\xa4\xa9\xe7\xa9\xba\xe8\xbf\x9b\xe9\x94\x80\xe5\xad\x98\xe7\xae\xa1\xe7\x90\x86\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe5\xb0\x98\xe6\x9c\x88\xe4\xbc\x81\xe4\xb8\x9a\xe7\xbd\x91\xe7\xab\x99\xe7\xae\xa1\xe7\x90\x86\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe5\xb0\x98\xe7\xbc\x98\xe9\x9b\x85\xe5\xa2\x83\xe5\x9b\xbe\xe6\x96\x87\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe5\xbb\xba\xe7\xab\x99\xe4\xb9\x8b\xe6\x98\x9f',
                   '\xe5\xbe\xae\xe6\x93\x8e\xe7\xa7\x91\xe6\x8a\x80', '\xe6\x82\x9f\xe7\xa9\xbacrm',
                   '\xe6\x82\x9f\xe7\xa9\xbacrm\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe6\x93\x8e\xe5\xa4\xa9\xe6\x94\xbf\xe5\x8a\xa1\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe6\x96\xb0\xe4\xb8\xba\xe8\xbd\xaf\xe4\xbb\xb6e-learning\xe7\xae\xa1\xe7\x90\x86\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe6\x96\xb0\xe7\xa7\x80', '\xe6\x96\xb9\xe7\xbb\xb4\xe5\x9b\xa2\xe8\xb4\xad',
                   '\xe6\x96\xb9\xe7\xbb\xb4\xe5\x9b\xa2\xe8\xb4\xad\xe8\xb4\xad\xe7\x89\xa9\xe5\x88\x86\xe4\xba\xab\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe6\x97\xb6\xe4\xbb\xa3\xe4\xbc\x81\xe4\xb8\x9a\xe9\x82\xae', '\xe6\x98\x8e\xe8\x85\xbecms',
                   '\xe6\x98\x93\xe5\x88\x9b\xe6\x80\x9d',
                   '\xe6\x98\x93\xe5\x88\x9b\xe6\x80\x9d\xe6\x95\x99\xe8\x82\xb2\xe5\xbb\xba\xe7\xab\x99\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe6\x98\x93\xe6\x83\xb3cms',
                   '\xe6\x99\xba\xe7\x9d\xbf\xe7\xbd\x91\xe7\xab\x99\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe6\x9c\x80\xe5\x9c\x9f\xe5\x9b\xa2\xe8\xb4\xad\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe6\x9c\xaa\xe7\x9f\xa5oem\xe5\xae\x89\xe9\x98\xb2\xe7\x9b\x91\xe6\x8e\xa7\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe6\x9c\xaa\xe7\x9f\xa5\xe6\x94\xbf\xe5\xba\x9c\xe9\x87\x87\xe8\xb4\xad\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe6\x9c\xaa\xe7\x9f\xa5\xe6\x9f\xa5\xe8\xaf\xa2\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe6\x9d\xad\xe5\xb7\x9e\xe5\x8d\x9a\xe9\x87\x87cms',
                   '\xe6\x9d\xb0\xe5\xa5\x87\xe5\xb0\x8f\xe8\xaf\xb4\xe8\xbf\x9e\xe8\xbd\xbd\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe6\xa1\x83\xe6\xba\x90\xe7\x9b\xb8\xe5\x86\x8c\xe7\xae\xa1\xe7\x90\x86\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe6\xb1\x87\xe6\x88\x90\xe4\xbc\x81\xe4\xb8\x9a\xe5\xbb\xba\xe7\xab\x99cms',
                   '\xe6\xb1\x87\xe6\x96\x87\xe5\x9b\xbe\xe4\xb9\xa6\xe9\xa6\x86\xe4\xb9\xa6\xe7\x9b\xae\xe6\xa3\x80\xe7\xb4\xa2\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe6\xb1\x89\xe7\xa0\x81\xe9\xab\x98\xe6\xa0\xa1\xe6\xaf\x95\xe4\xb8\x9a\xe7\x94\x9f\xe5\xb0\xb1\xe4\xb8\x9a\xe4\xbf\xa1\xe6\x81\xaf\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe6\xb3\x9b\xe5\xbe\xaee-office', '\xe6\xb3\x9b\xe5\xbe\xaeoa', '\xe6\xb5\xaa\xe6\xbd\xaecms',
                   '\xe6\xb5\xb7\xe5\xba\xb7\xe5\xa8\x81\xe8\xa7\x86', '\xe7\x88\xb1\xe6\xb7\x98\xe5\xae\xa2',
                   '\xe7\x88\xb1\xe8\xa3\x85\xe7\xbd\x91',
                   '\xe7\x94\xa8\xe5\x8f\x8bfe\xe5\x8d\x8f\xe4\xbd\x9c\xe5\x8a\x9e\xe5\x85\xac\xe5\xb9\xb3\xe5\x8f\xb0',
                   '\xe7\x94\xa8\xe5\x8f\x8bfe\xe7\xae\xa1\xe7\x90\x86\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe7\x94\xa8\xe5\x8f\x8bturbcrm\xe7\xb3\xbb\xe7\xbb\x9f', '\xe7\x94\xa8\xe5\x8f\x8bu8',
                   '\xe7\x94\xa8\xe5\x8f\x8b',
                   '\xe7\x9a\x93\xe7\xbf\xb0\xe9\x80\x9a\xe7\x94\xa8\xe6\x95\xb0\xe5\xad\x97\xe5\x8c\x96\xe6\xa0\xa1\xe5\x9b\xad\xe5\xb9\xb3\xe5\x8f\xb0',
                   '\xe7\x9c\x81\xe7\xba\xa7\xe5\x86\x9c\xe6\x9c\xba\xe6\x9e\x84\xe7\xbd\xae\xe8\xa1\xa5\xe8\xb4\xb4\xe4\xbf\xa1\xe6\x81\xaf\xe7\xae\xa1\xe7\x90\x86\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe7\xa7\x91\xe4\xbf\xa1\xe9\x82\xae\xe4\xbb\xb6\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe7\xa7\x91\xe8\xbf\x88ras', '\xe7\xa8\x8b\xe6\xb0\x8f\xe8\x88\x9e\xe6\x9b\xb2cms',
                   '\xe7\xbb\xbf\xe9\xba\xbb\xe9\x9b\x80\xe5\x80\x9f\xe8\xb4\xb7\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe7\xbd\x91\xe8\xb6\xa3\xe5\x95\x86\xe5\x9f\x8e',
                   '\xe7\xbd\x91\xe9\x92\x9b\xe6\x96\x87\xe7\xab\xa0\xe7\xae\xa1\xe7\x90\x86\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe8\x80\x81y\xe6\x96\x87\xe7\xab\xa0\xe7\xae\xa1\xe7\x90\x86\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe8\x81\x94\xe4\xbc\x97mediinfo\xe5\x8c\xbb\xe9\x99\xa2\xe7\xbb\xbc\xe5\x90\x88\xe7\xae\xa1\xe7\x90\x86\xe5\xb9\xb3\xe5\x8f\xb0',
                   '\xe8\x87\xaa\xe5\x8a\xa8\xe5\x8f\x91\xe5\x8d\xa1\xe5\xb9\xb3\xe5\x8f\xb0',
                   '\xe8\x89\xaf\xe7\xb2\xbe\xe5\x8d\x97\xe6\x96\xb9', '\xe8\x89\xba\xe5\xb8\x86cms',
                   '\xe8\x8f\xb2\xe6\x96\xaf\xe7\x89\xb9\xe8\xaf\xba\xe6\x9c\x9f\xe5\x88\x8a\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe8\x93\x9d\xe5\x87\x8ceis\xe6\x99\xba\xe6\x85\xa7\xe5\x8d\x8f\xe5\x90\x8c\xe5\xb9\xb3\xe5\x8f\xb0',
                   '\xe8\x93\x9d\xe7\xa7\x91cms',
                   '\xe8\x96\x84\xe5\x86\xb0\xe6\x97\xb6\xe6\x9c\x9f\xe7\xbd\x91\xe7\xab\x99\xe7\xae\xa1\xe7\x90\x86\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe8\xae\xaf\xe6\x97\xb6\xe7\xbd\x91\xe7\xab\x99\xe7\xae\xa1\xe7\x90\x86\xe7\xb3\xbb\xe7\xbb\x9fcms',
                   '\xe8\xae\xb0\xe4\xba\x8b\xe7\x8b\x97',
                   '\xe8\xb4\xb7\xe9\xbd\x90\xe4\xb9\x90\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe9\x80\x9a\xe8\xbe\xbeoa\xe7\xb3\xbb\xe7\xbb\x9f', '\xe9\x80\x9f\xe8\xb4\x9dcms',
                   '\xe9\x87\x91\xe8\x89\xb2\xe6\xa0\xa1\xe5\x9b\xad', '\xe9\x87\x91\xe8\x9d\xb6oa',
                   '\xe9\x87\x91\xe8\x9d\xb6\xe5\x8d\x8f\xe4\xbd\x9c\xe5\x8a\x9e\xe5\x85\xac\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe9\x87\x91\xe9\x92\xb1\xe6\x9f\x9cp2p',
                   '\xe9\x9b\x86\xe6\x97\xb6\xe9\x80\x9a\xe8\xae\xaf\xe7\xa8\x8b\xe5\xba\x8f',
                   '\xe9\x9c\xb2\xe7\x8f\xa0\xe6\x96\x87\xe7\xab\xa0\xe7\xae\xa1\xe7\x90\x86\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe9\x9d\x92\xe4\xba\x91\xe5\xae\xa2cms',
                   '\xe9\x9d\x92\xe5\xb3\xb0\xe7\xbd\x91\xe7\xbb\x9c\xe6\x99\xba\xe8\x83\xbd\xe7\xbd\x91\xe7\xab\x99\xe7\xae\xa1\xe7\x90\x86\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe9\x9d\x92\xe6\x9e\x9c\xe5\xad\xa6\xe7\x94\x9f\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe9\x9d\x92\xe6\x9e\x9c\xe5\xad\xa6\xe7\x94\x9f\xe7\xbb\xbc\xe5\x90\x88\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe9\x9d\x92\xe6\x9e\x9c\xe6\x95\x99\xe5\x8a\xa1\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe9\x9d\x92\xe6\x9e\x9c\xe8\xbd\xaf\xe4\xbb\xb6\xe6\x95\x99\xe5\x8a\xa1\xe7\xb3\xbb\xe7\xbb\x9f',
                   '\xe9\x9d\x9e\xe5\x87\xa1\xe5\xbb\xba\xe7\xab\x99']


user_agent = ['Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.8.1) Gecko/20061010 Firefox/2.0',
                  'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.6 Safari/532.0',
                  'Mozilla/5.0 (Windows; U; Windows NT 5.1 ; x64; en-US; rv:1.9.1b2pre) Gecko/20081026 Firefox/3.1b2pre',
                  'Opera/10.60 (Windows NT 5.1; U; zh-cn) Presto/2.6.30 Version/10.60',
                  'Opera/8.01 (J2ME/MIDP; Opera Mini/2.0.4062; en; U; ssr)',
                  'Mozilla/5.0 (Windows; U; Windows NT 5.1; ; rv:1.9.0.14) Gecko/2009082707 Firefox/3.0.14',
                  'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
                  'Mozilla/5.0 (Windows; U; Windows NT 6.0; fr; rv:1.9.2.4) Gecko/20100523 Firefox/3.6.4 ( .NET CLR 3.5.30729)',
                  'Mozilla/5.0 (Windows; U; Windows NT 6.0; fr-FR) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16',
                  'Mozilla/5.0 (Windows; U; Windows NT 6.0; fr-FR) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5']




def get_request_headers():

    UA = random.choice(user_agent)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent': UA,
        'Upgrade-Insecure-Requests': '1', 'Connection': 'keep-alive', 'Cache-Control': 'max-age=0',
        'Accept-Encoding': 'gzip, deflate, sdch', 'Accept-Language': 'zh-CN,zh;q=0.8',
        "Referer": "http://www.baidu.com/link?url=www.so.com&url=www.soso.com&&url=www.sogou.com",
        'Cookie': "PHPSESSID=gljsd5c3ei5n813roo4878q203"
        }
    
    return headers



pwd = os.getcwd()

def check(_id):

    with sqlite3.connect(pwd+'/cms_finger.db') as conn:

        cursor  = conn.cursor()
        result = cursor.execute(f"SELECT name, keys From `tide` WHERE  id= '{_id}'")
        for row in result:
            return row[0], row[1]

def count():
    with sqlite3.connect(pwd+'/cms_finger.db') as conn:

        cursor = conn.cursor()
        result=  cursor.execute('select count(id) from tide')

        for row in result:
            return row[0]

# ! re 设置匹配的格式

rtitle = re.compile(r'title="(.*)"')
rheader = re.compile(r'header="(.*)"')
rbody = re.compile(r'body="(.*)"')
rbracket = re.compile(r'\((.*)\)')

if __name__ == "__main__":
    name , keys =check(2)
    print(name)
    print(keys)
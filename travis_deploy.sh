cd databags
mv navigation.json navigation_local.json
ln -s navigation_deploy.json navigation.json
cd ..

eval $(ssh-agent -s)
mv content/ content_root/
ln -s content_root/help content

openssl aes-256-cbc -K $encrypted_1c9ebd4878cf_key -iv $encrypted_1c9ebd4878cf_iv -in deploy_keys.tar.enc -out deploy_keys.tar -d
tar xvf deploy_keys.tar

lektor clean --yes
lektor build
ls -l
ssh-add -D
ssh-add ./deploy_key_help
lektor deploy ghpageshelp --key-file ${TRAVIS_BUILD_DIR}/deploy_key_help
rm content

ln -s content_root/about content
lektor clean --yes
lektor build
ssh-add -D
ssh-add ./deploy_key_about
lektor deploy ghpagesabout --key-file ${TRAVIS_BUILD_DIR}/deploy_key_about
rm content

ln -s content_root/blog content
lektor clean --yes
lektor build
ssh-add -D
ssh-add ./deploy_key_blog
lektor deploy ghpagesblog --key-file ${TRAVIS_BUILD_DIR}/deploy_key_blog
rm content

mv content_root/ content/
rm databags/navigation.json
mv databags/navigation_local.json databags/navigation.json

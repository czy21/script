use admin;
db.system.users.remove({
    user: "admin"
});
db.createUser({
    user: "admin",
    pwd: "Dev.6411",
    roles: [{
        role: "userAdminAnyDatabase",
        db: "admin"
    }]
});
db.system.users.find();

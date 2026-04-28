const player = new Plyr("#player",{
    controls:[
        "play-large",
        "play",
        "progress",
        "current-time",
        "duration",
        "mute",
        "volume",
        'settings',
        'fullscreen'
    ],
    settings:['quality','speed'],
    speed:{selected:1,options:[0.5,0.75,1,1.25,2]},
    tooltips:{controls:true,seek:true},
    storage:{enabled:true,key:"plyr"}
});
bind pub -|- !nukestats nukestats
proc nukestats {nick uhost hand chan args} {
    set nukestats {/mnt/glftpd/bin/nukes.py}
    set nickname $nick 
        if {[llength $args] > 0} {
        set nickname [lindex $args 0] 
    }
    set msgthis [catch {exec python3 $nukestats $nickname} output]
    if {$msgthis != 0} {
        putquick "PRIVMSG $chan :Error when executing the script: $output"
        return
    }
    foreach line [split $output "\n"] {
        putquick "PRIVMSG $nick :$line"
    }
}
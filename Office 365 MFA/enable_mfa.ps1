#very bare bones

Connect-ExchangeOnline
Connect-MsolService

$mf= New-Object -TypeName Microsoft.Online.Administration.StrongAuthenticationRequirement
$mf.RelyingParty = "*"
$mfa = @($mf)

$list = @() #input your string array of names


foreach ($user in $list) {
    Get-MsolUser -SearchString $user | Set-MsolUser -StrongAuthenticationRequirements $mfa
}

foreach ($user in $list)
{
    Get-MsolUser -SearchString $user | Select-Object UserPrincipalName,StrongAuthenticationRequirements
}
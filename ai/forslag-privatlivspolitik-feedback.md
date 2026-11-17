# Forslag til privatlivspolitikken: AI læser feedback (til Jonas' godkendelse)

`privatlivspolitik.html` hører til grundloven, så jeg har IKKE ændret den. Her er forslag til tekst. Du bør selv vurdere ordlyden (og eventuelt få den set igennem), fordi den handler om GDPR og en databehandler i USA.

## Hvad der sker
Beskeder fra feedback-chatten læses hver morgen af en AI (Claude, fra Anthropic), som sorterer dem og vurderer, om de kan bruges til at rette fejl eller forbedre siden. AI'en får beskedens tekst, typen, siden og den tekniske baggrund (butik, valgte retter, skærmstørrelse). Den får **aldrig e-mailadressen**. Resultatet er en omskrevet opsummering uden personoplysninger. Rå beskeder gemmes ikke i den offentlige kode.

## Forslag: tilføj under "Feedback, du selv sender" (afsnit om hvad vi indsamler)
> Din besked i feedback-chatten bliver læst af en AI-assistent (Claude fra Anthropic), som sorterer beskeder og vurderer, om de kan bruges til at forbedre siden. Assistenten får ikke din e-mailadresse. Skriv derfor ikke navne eller andre personoplysninger i selve beskeden.

## Forslag: tilføj til listen over databehandlere
> **Anthropic** (AI-assistent, der sorterer feedback-beskeder). Behandlingen sker uden din e-mailadresse. Dataene kan blive behandlet uden for EU (USA).

## Det skal du vurdere
- Om Anthropics vilkår for databehandling og overførsel uden for EU er dækket for din kontoform (privat konto).
- Om beskeder skal slettes efter et vist antal dage. Nu gemmes de i Supabase, indtil du sletter dem (stå som "Feedback gemmes, indtil den er behandlet" i politikken). Agenten markerer dem kun som "læst" i en egen kolonne (`agent_set`); den sletter ingenting.

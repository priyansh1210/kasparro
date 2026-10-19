# Run 30c6971f-0955-41a8-b4b9-89298786a67e (v1 / development)

- status: completed
- provider/model: gemini / gemini-2.5-flash
- settings: `{"provider": "gemini", "model": "gemini-2.5-flash", "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/", "request_timeout_s": 120.0, "temperature": 0.0, "transient_retries": 6, "max_model_turns": 3, "output_mode": "quote", "workers": 10}`
- prompt_hash: `972d55ca3052be90e4301f0667734a1e73cf7c08dd27da5a4560158d9b65ab8b`
- source_hash: `df1d1720593796d621ded8c7f1fe43a415ecd1447e620eb085f563c1967f1870`
- versions: dataset long-brand-answers-50-v4, facts speaker-catalogue-v4, evaluator sentence-spans-and-labels-v4
- file hashes: `{"answers.csv": "fa28e813ea54b4e5ea985585f22f084d826241e1182accbc27ace17066125724", "brand_facts.csv": "2190d40fad2dd167ef2437956c43d595aaf2554ea673a4789b9343cb7e2936f2", "development_gold.csv": "afe84cc78f304afb6a4aaa505dd7504af80fcbf8bc507806aa5ff0aab6bf4850"}`
- started 2026-10-19T10:15:45.186682+00:00 finished 2026-10-19T10:15:47.224066+00:00

## Counts

answers scheduled 40, ok 0, error 40 {'provider_error': 40}, empty 0; G=376 P=0 M=0 C=0

## Metrics

| | precision | recall | F1 |
|---|---|---|---|
| extraction | 0.0000 | 0.0000 | 0.0000 |
| joint (main) | 0.0000 | 0.0000 | 0.0000 |

coverage C/G = 0.0000

## Missed gold claims

- `A01:306:460` [supported] For the current India catalogue, ClearTrail Mini is listed at INR 1,200 less than ClearTrail Plus, comparing the two tax-inclusive prices before shipping.
- `A01:461:647` [contradicted] For an authorized India purchase with the original invoice and a manufacturing defect, ClearTrail Mini receives a standard manufacturer warranty lasting 18 months from the purchase date.
- `A01:649:832` [unknown] An opened ClearTrail Mini can be returned to any authorized India seller within thirty days for a full refund, even when the speaker has no manufacturing defect or functional problem.
- `A01:833:1040` [unknown] The sustained amplifier output of ClearTrail Mini is forty watts per channel during ordinary playback, which allows a direct loudness comparison with other speakers advertised using electrical power figures.
- `A01:1237:1439` [unknown] An authorized India service centre guarantees repair of ClearTrail Mini within two working days after receiving the unit and the required purchase paperwork, regardless of replacement-part availability.
- `A01:1440:1619` [contradicted] The stated laboratory playback time for ClearTrail Mini, using a new battery with EQ off at one hundred percent volume, remains 12 hours without any reduction for louder playback.
- `A01:1620:1767` [supported] For an India purchase at the official catalogue list price on 1 October 2026, ClearTrail Mini costs INR 1,299 including tax but excluding shipping.
- `A01:1769:1942` [contradicted] The official India retail box for ClearTrail Mini includes a wall charging adapter, even though separate accessory lists may make the charging arrangement look less obvious.
- `A01:1943:2104` [supported] The built-in Wi-Fi capability of ClearTrail Mini is absent, which should be treated as a separate specification from its ability to receive audio over Bluetooth.
- `A02:306:506` [supported] Whatever conclusions a buyer draws from the water-resistance rating, water damage remains excluded from the standard India manufacturer warranty covering CloudNote Studio after an authorized purchase.
- `A02:507:689` [contradicted] The official India retail box for CloudNote Studio does not include a wall charging adapter, even though separate accessory lists may make the charging arrangement look less obvious.
- `A02:691:875` [unknown] An opened CloudNote Studio can be returned to any authorized India seller within thirty days for a full refund, even when the speaker has no manufacturing defect or functional problem.
- `A02:876:1084` [unknown] The sustained amplifier output of CloudNote Studio is forty watts per channel during ordinary playback, which allows a direct loudness comparison with other speakers advertised using electrical power figures.
- `A02:1085:1272` [unknown] CloudNote Studio supports the AAC Bluetooth audio codec on compatible phones, so its published Bluetooth version can be treated as evidence for that specific audio-compression capability.
- `A02:1469:1659` [unknown] In winter weather below freezing, CloudNote Studio delivers its full 18-hour laboratory battery duration at fifty percent volume, without the outdoor temperature changing the stated runtime.
- `A02:1660:1813` [supported] For the current India catalogue, CloudNote Studio is listed at INR 1,500 more than CloudNote Air, comparing the two tax-inclusive prices before shipping.
- `A02:1815:2039` [contradicted] Water damage to CloudNote Studio is included in the standard India manufacturer warranty after an authorized purchase, because water resistance should be understood as warranty coverage rather than just a product capability.
- `A02:2040:2223` [contradicted] The manufacturer supports a stereo pair made from one CloudNote Studio and one CloudNote Air, since being members of the same brand is sufficient for cross-model stereo compatibility.
- `A02:2224:2372` [supported] For an India purchase at the official catalogue list price on 1 October 2026, CloudNote Studio costs INR 2,999 including tax but excluding shipping.
- `A03:335:505` [unknown] Orders for CloudNote Air receive free delivery to every India postal code, so there is no separate shipping charge even when a customer selects a remote delivery address.
- `A03:506:687` [unknown] An opened CloudNote Air can be returned to any authorized India seller within thirty days for a full refund, even when the speaker has no manufacturing defect or functional problem.
- `A03:689:861` [supported] The built-in microphone is included on CloudNote Air, so microphone availability should be checked for this exact model instead of copied from another speaker in the range.
- `A03:862:1043` [supported] Considering the speaker alone and leaving retail packaging and accessories out of the measurement, CloudNote Air has a stated mass of 0.35 kilograms for carrying-weight comparisons.
- `A03:1240:1409` [contradicted] The built-in microphone is not included on CloudNote Air, without needing an accessory to change the hardware specification being described for this exact speaker model.
- `A03:1410:1563` [supported] For the current India catalogue, CloudNote Air is listed at INR 1,500 less than CloudNote Studio, comparing the two tax-inclusive prices before shipping.
- `A03:1564:1742` [contradicted] When measuring just the speaker rather than the retail box and accessories, CloudNote Air weighs 1100 grams, matching the carrying-weight figure associated with CloudNote Studio.
- `A03:1744:1917` [supported] Despite the declared IPX4 water-resistance rating, the manufacturer does not permit fresh-water immersion of CloudNote Air, even with all of the port covers properly closed.
- `A03:1918:2069` [contradicted] For an India purchase at the official catalogue list price on 1 October 2026, CloudNote Air still costs INR 1,199 including tax but excluding shipping.
- `A04:324:493` [contradicted] The built-in microphone is not included on StoneWave Max, without needing an accessory to change the hardware specification being described for this exact speaker model.
- `A04:494:694` [unknown] An authorized India service centre guarantees repair of StoneWave Max within two working days after receiving the unit and the required purchase paperwork, regardless of replacement-part availability.
- `A04:696:899` [unknown] A retail purchase of StoneWave Max in Germany qualifies for the same 18-month manufacturer warranty described for authorized India purchases, without any different regional terms affecting that duration.
- `A04:900:1097` [supported] Whatever conclusions a buyer draws from the water-resistance rating, water damage remains excluded from the standard India manufacturer warranty covering StoneWave Max after an authorized purchase.
- `A04:1098:1267` [supported] The move from the 2025 India catalogue to the 2026 catalogue raised the tax-inclusive list price of StoneWave Max by INR 200, with shipping excluded in both comparisons.
- `A04:1464:1636` [supported] For wired digital audio specifically, the USB-C connector on StoneWave Max does provide an audio-input path, regardless of the fact that the connector also serves charging.
- `A04:1637:1798` [contradicted] At fifty percent volume with EQ off and a new battery in the laboratory, StoneWave Max is rated for 1500 minutes of playback before recharging becomes necessary.
- `A04:1800:1983` [contradicted] With all port covers closed, StoneWave Max is permitted to remain immersed in fresh water at a depth of one metre for a full hour under the manufacturer's stated laboratory allowance.
- `A04:1984:2165` [unknown] An opened StoneWave Max can be returned to any authorized India seller within thirty days for a full refund, even when the speaker has no manufacturing defect or functional problem.
- `A04:2166:2361` [unknown] StoneWave Max accepts two active Bluetooth source connections at the same time and switches between them automatically, without asking the listener to disconnect one phone before using the other.
- `A04:2363:2540` [contradicted] In the 2025 India catalogue, before the current-year revision, StoneWave Max already carried the same tax-inclusive list price of INR 3,499, excluding shipping from that amount.
- `A05:371:531` [contradicted] At fifty percent volume with EQ off and a new battery in the laboratory, StoneWave Go is rated for 1020 minutes of playback before recharging becomes necessary.
- `A05:532:697` [supported] The official India retail box for StoneWave Go does not contain a wall charging adapter, so the box contents should not be inferred just from the charging-port type.
- `A05:699:890` [unknown] The Bluetooth connection on StoneWave Go maintains uninterrupted playback at a distance of one hundred metres outdoors, even when a listener changes the phone used as the transmitting device.
- `A05:891:1095` [unknown] The sustained amplifier output of StoneWave Go is forty watts per channel during ordinary playback, which allows a direct loudness comparison with other speakers advertised using electrical power figures.
- `A05:1292:1467` [supported] The built-in microphone is not included on StoneWave Go, so microphone availability should be checked for this exact model instead of copied from another speaker in the range.
- `A05:1468:1651` [contradicted] Basic Bluetooth playback on StoneWave Go requires the manufacturer companion app to be installed first, rather than allowing a listener to pair a source and start playback without it.
- `A05:1652:1828` [unknown] Using a twenty-watt wall adapter, a fully discharged StoneWave Go reaches a complete charge in ninety minutes, so a short charging stop is enough to restore the entire battery.
- `A05:1830:1980` [contradicted] For an India purchase at the official catalogue list price on 1 October 2026, StoneWave Go still costs INR 1,799 including tax but excluding shipping.
- `A06:306:494` [contradicted] For wired digital audio specifically, the USB-C connector on ClearTrail Plus does not provide an audio-input path, so the connector can be treated accordingly when choosing a wired source.
- `A06:495:697` [unknown] No version of ClearTrail Plus has ever been offered in blue, including previous-year retail stock and editions supplied only through independent authorized sellers rather than the official online store.
- `A06:699:897` [unknown] The plastic used in the enclosure of ClearTrail Plus contains at least sixty percent post-consumer recycled material by weight, excluding the electronic components and the external retail packaging.
- `A06:898:1081` [unknown] The official India catalogue price of ClearTrail Plus will drop by INR 300 during January 2027, with that future reduction applying before shipping to purchases from the brand itself.
- `A06:1082:1235` [contradicted] For an India purchase at the official catalogue list price on 1 October 2026, ClearTrail Plus still costs INR 2,199 including tax but excluding shipping.
- `A06:1432:1621` [unknown] In winter weather below freezing, ClearTrail Plus delivers its full 20-hour laboratory battery duration at fifty percent volume, without the outdoor temperature changing the stated runtime.
- `A06:1622:1801` [contradicted] The stated laboratory playback time for ClearTrail Plus, using a new battery with EQ off at one hundred percent volume, remains 20 hours without any reduction for louder playback.
- `A06:1803:1957` [supported] For the current India catalogue, ClearTrail Plus is listed at INR 1,200 more than ClearTrail Mini, comparing the two tax-inclusive prices before shipping.
- `A06:1958:2132` [supported] The built-in microphone is included on ClearTrail Plus, so microphone availability should be checked for this exact model instead of copied from another speaker in the range.
- `A06:2133:2356` [contradicted] Water damage to ClearTrail Plus is included in the standard India manufacturer warranty after an authorized purchase, because water resistance should be understood as warranty coverage rather than just a product capability.
- `A07:306:511` [unknown] A retail purchase of ClearTrail Plus in Germany qualifies for the same 12-month manufacturer warranty described for authorized India purchases, without any different regional terms affecting that duration.
- `A07:512:698` [unknown] ClearTrail Plus supports the AAC Bluetooth audio codec on compatible phones, so its published Bluetooth version can be treated as evidence for that specific audio-compression capability.
- `A07:700:884` [contradicted] The manufacturer supports a stereo pair made from one ClearTrail Plus and one ClearTrail Mini, since being members of the same brand is sufficient for cross-model stereo compatibility.
- `A07:987:1153` [supported] With all port covers closed, the laboratory immersion allowance for ClearTrail Plus is limited to fresh water at no more than one metre for no more than half an hour.
- `A07:1350:1533` [supported] Considering the speaker alone and leaving retail packaging and accessories out of the measurement, ClearTrail Plus has a stated mass of 0.58 kilograms for carrying-weight comparisons.
- `A07:1534:1719` [supported] Basic Bluetooth listening on ClearTrail Plus does not require the manufacturer companion app to be installed, even if a buyer is interested in optional app-related features or settings.
- `A07:1721:1919` [unknown] The plastic used in the enclosure of ClearTrail Plus contains at least sixty percent post-consumer recycled material by weight, excluding the electronic components and the external retail packaging.
- `A07:1920:2143` [contradicted] Water damage to ClearTrail Plus is included in the standard India manufacturer warranty after an authorized purchase, because water resistance should be understood as warranty coverage rather than just a product capability.
- `A08:335:525` [supported] Even when other warranty conditions are met for an authorized India purchase, the original purchase invoice is still required to claim the standard manufacturer warranty for ClearTrail Mini.
- `A08:526:685` [contradicted] The built-in Wi-Fi capability of ClearTrail Mini is present, independently of whatever Bluetooth connection a listener might also choose for everyday playback.
- `A08:687:889` [unknown] An authorized India service centre guarantees repair of ClearTrail Mini within two working days after receiving the unit and the required purchase paperwork, regardless of replacement-part availability.
- `A08:890:1083` [supported] The manufacturer permits stereo pairing only between two units of the exact ClearTrail Mini model, rather than treating every speaker sharing the same brand name as a compatible stereo partner.
- `A08:1084:1282` [unknown] The plastic used in the enclosure of ClearTrail Mini contains at least sixty percent post-consumer recycled material by weight, excluding the electronic components and the external retail packaging.
- `A08:1479:1676` [unknown] ClearTrail Mini accepts two active Bluetooth source connections at the same time and switches between them automatically, without asking the listener to disconnect one phone before using the other.
- `A08:1677:1855` [supported] For wired digital audio specifically, the USB-C connector on ClearTrail Mini does not provide an audio-input path, regardless of the fact that the connector also serves charging.
- `A08:1857:2036` [contradicted] An original invoice is unnecessary when claiming the standard India manufacturer warranty for ClearTrail Mini, provided the buyer says the purchase came from an authorized seller.
- `A08:2037:2200` [supported] Looking back specifically at the 2025 India catalogue rather than the current offer, the listed tax-inclusive price of ClearTrail Mini was INR 999 before shipping.
- `A08:2201:2395` [unknown] The normal manufacturing origin of ClearTrail Mini is India, even when the unit is purchased through an authorized seller rather than ordered directly from the manufacturer's own retail channel.
- `A09:324:491` [supported] With all port covers closed, the laboratory immersion allowance for CloudNote Studio is limited to fresh water at no more than one metre for no more than half an hour.
- `A09:492:655` [contradicted] For a current India catalogue comparison before shipping, CloudNote Studio is INR 1,500 less expensive than CloudNote Air, with tax included in both listed prices.
- `A09:657:844` [unknown] CloudNote Studio supports the AAC Bluetooth audio codec on compatible phones, so its published Bluetooth version can be treated as evidence for that specific audio-compression capability.
- `A09:845:1048` [unknown] An authorized India service centre guarantees repair of CloudNote Studio within two working days after receiving the unit and the required purchase paperwork, regardless of replacement-part availability.
- `A09:1245:1430` [supported] With a new battery, EQ disabled and volume held at fifty percent in the laboratory, CloudNote Studio has a stated playback duration of 1080 minutes under those specific test conditions.
- `A09:1431:1614` [contradicted] The manufacturer supports a stereo pair made from one CloudNote Studio and one CloudNote Air, since being members of the same brand is sufficient for cross-model stereo compatibility.
- `A09:1615:1781` [supported] Looking back specifically at the 2025 India catalogue rather than the current offer, the listed tax-inclusive price of CloudNote Studio was INR 2,799 before shipping.
- `A09:1783:1963` [contradicted] An original invoice is unnecessary when claiming the standard India manufacturer warranty for CloudNote Studio, provided the buyer says the purchase came from an authorized seller.
- `A09:1964:2148` [unknown] An opened CloudNote Studio can be returned to any authorized India seller within thirty days for a full refund, even when the speaker has no manufacturing defect or functional problem.
- `A10:371:563` [unknown] The normal manufacturing origin of CloudNote Air is India, even when the unit is purchased through an authorized seller rather than ordered directly from the manufacturer's own retail channel.
- `A10:564:733` [supported] The move from the 2025 India catalogue to the 2026 catalogue raised the tax-inclusive list price of CloudNote Air by INR 300, with shipping excluded in both comparisons.
- `A10:735:923` [supported] Even when other warranty conditions are met for an authorized India purchase, the original purchase invoice is still required to claim the standard manufacturer warranty for CloudNote Air.
- `A10:924:1087` [supported] Looking back specifically at the 2025 India catalogue rather than the current offer, the listed tax-inclusive price of CloudNote Air was INR 1,199 before shipping.
- `A10:1088:1265` [contradicted] An original invoice is unnecessary when claiming the standard India manufacturer warranty for CloudNote Air, provided the buyer says the purchase came from an authorized seller.
- `A10:1462:1643` [unknown] The official India catalogue price of CloudNote Air will drop by INR 300 during January 2027, with that future reduction applying before shipping to purchases from the brand itself.
- `A10:1644:1821` [contradicted] In the 2025 India catalogue, before the current-year revision, CloudNote Air already carried the same tax-inclusive list price of INR 1,499, excluding shipping from that amount.
- `A10:1823:2004` [unknown] An opened CloudNote Air can be returned to any authorized India seller within thirty days for a full refund, even when the speaker has no manufacturing defect or functional problem.
- `A10:2005:2200` [unknown] CloudNote Air accepts two active Bluetooth source connections at the same time and switches between them automatically, without asking the listener to disconnect one phone before using the other.
- `A10:2201:2372` [contradicted] The official India retail box for CloudNote Air includes a wall charging adapter, even though separate accessory lists may make the charging arrangement look less obvious.
- `A11:306:483` [contradicted] In the 2025 India catalogue, before the current-year revision, StoneWave Max already carried the same tax-inclusive list price of INR 3,499, excluding shipping from that amount.
- `A11:484:653` [contradicted] The built-in microphone is not included on StoneWave Max, without needing an accessory to change the hardware specification being described for this exact speaker model.
- `A11:655:855` [unknown] An authorized India service centre guarantees repair of StoneWave Max within two working days after receiving the unit and the required purchase paperwork, regardless of replacement-part availability.
- `A11:856:1026` [unknown] Orders for StoneWave Max receive free delivery to every India postal code, so there is no separate shipping charge even when a customer selects a remote delivery address.
- `A11:1027:1172` [supported] For an India purchase at the official catalogue list price on 1 October 2026, StoneWave Max costs INR 3,499 including tax but excluding shipping.
- `A11:1369:1532` [supported] Looking back specifically at the 2025 India catalogue rather than the current offer, the listed tax-inclusive price of StoneWave Max was INR 3,299 before shipping.
- `A11:1533:1697` [supported] With all port covers closed, the laboratory immersion allowance for StoneWave Max is limited to fresh water at no more than one metre for no more than half an hour.
- `A11:1699:1895` [unknown] The plastic used in the enclosure of StoneWave Max contains at least sixty percent post-consumer recycled material by weight, excluding the electronic components and the external retail packaging.
- `A11:1896:2091` [unknown] StoneWave Max accepts two active Bluetooth source connections at the same time and switches between them automatically, without asking the listener to disconnect one phone before using the other.
- `A11:2092:2264` [supported] The built-in microphone is included on StoneWave Max, so microphone availability should be checked for this exact model instead of copied from another speaker in the range.
- `A12:335:515` [unknown] The official India catalogue price of StoneWave Go will drop by INR 300 during January 2027, with that future reduction applying before shipping to purchases from the brand itself.
- `A12:516:674` [supported] The built-in Wi-Fi capability of StoneWave Go is absent, which should be treated as a separate specification from its ability to receive audio over Bluetooth.
- `A12:676:871` [unknown] The plastic used in the enclosure of StoneWave Go contains at least sixty percent post-consumer recycled material by weight, excluding the electronic components and the external retail packaging.
- `A12:872:1032` [contradicted] At fifty percent volume with EQ off and a new battery in the laboratory, StoneWave Go is rated for 1020 minutes of playback before recharging becomes necessary.
- `A12:1229:1378` [supported] For the current India catalogue, StoneWave Go is listed at INR 1,500 less than StoneWave Max, comparing the two tax-inclusive prices before shipping.
- `A12:1379:1559` [unknown] An opened StoneWave Go can be returned to any authorized India seller within thirty days for a full refund, even when the speaker has no manufacturing defect or functional problem.
- `A12:1560:1741` [contradicted] For wired digital audio specifically, the USB-C connector on StoneWave Go does provide an audio-input path, so the connector can be treated accordingly when choosing a wired source.
- `A12:1743:1916` [contradicted] When measuring just the speaker rather than the retail box and accessories, StoneWave Go weighs 900 grams, matching the carrying-weight figure associated with StoneWave Max.
- `A12:1917:2113` [supported] Whatever conclusions a buyer draws from the water-resistance rating, water damage remains excluded from the standard India manufacturer warranty covering StoneWave Go after an authorized purchase.
- `A13:324:510` [unknown] In winter weather below freezing, StoneWave Go delivers its full 16-hour laboratory battery duration at fifty percent volume, without the outdoor temperature changing the stated runtime.
- `A13:511:680` [unknown] Orders for StoneWave Go receive free delivery to every India postal code, so there is no separate shipping charge even when a customer selects a remote delivery address.
- `A13:682:902` [contradicted] Water damage to StoneWave Go is included in the standard India manufacturer warranty after an authorized purchase, because water resistance should be understood as warranty coverage rather than just a product capability.
- `A13:903:1067` [contradicted] The built-in microphone is included on StoneWave Go, without needing an accessory to change the hardware specification being described for this exact speaker model.
- `A13:1068:1270` [unknown] A retail purchase of StoneWave Go in Germany qualifies for the same 18-month manufacturer warranty described for authorized India purchases, without any different regional terms affecting that duration.
- `A13:1467:1623` [contradicted] The built-in Wi-Fi capability of StoneWave Go is present, independently of whatever Bluetooth connection a listener might also choose for everyday playback.
- `A13:1624:1804` [supported] With a new battery, EQ disabled and volume held at fifty percent in the laboratory, StoneWave Go has a stated playback duration of 960 minutes under those specific test conditions.
- `A13:1806:1950` [supported] For an India purchase at the official catalogue list price on 1 October 2026, StoneWave Go costs INR 1,999 including tax but excluding shipping.
- `A13:1951:2126` [supported] For wired digital audio specifically, the USB-C connector on StoneWave Go does not provide an audio-input path, regardless of the fact that the connector also serves charging.
- `A13:2127:2307` [unknown] An opened StoneWave Go can be returned to any authorized India seller within thirty days for a full refund, even when the speaker has no manufacturing defect or functional problem.
- `A14:371:557` [unknown] ClearTrail Plus supports the AAC Bluetooth audio codec on compatible phones, so its published Bluetooth version can be treated as evidence for that specific audio-compression capability.
- `A14:558:756` [unknown] The plastic used in the enclosure of ClearTrail Plus contains at least sixty percent post-consumer recycled material by weight, excluding the electronic components and the external retail packaging.
- `A14:758:943` [contradicted] With all port covers closed, ClearTrail Plus is permitted to remain immersed in fresh water at a depth of one metre for a full hour under the manufacturer's stated laboratory allowance.
- `A14:944:1127` [unknown] The official India catalogue price of ClearTrail Plus will drop by INR 300 during January 2027, with that future reduction applying before shipping to purchases from the brand itself.
- `A14:1324:1471` [supported] For an India purchase at the official catalogue list price on 1 October 2026, ClearTrail Plus costs INR 2,499 including tax but excluding shipping.
- `A14:1472:1662` [supported] Even when other warranty conditions are met for an authorized India purchase, the original purchase invoice is still required to claim the standard manufacturer warranty for ClearTrail Plus.
- `A14:1663:1837` [supported] For wired digital audio specifically, the USB-C connector on ClearTrail Plus does provide an audio-input path, regardless of the fact that the connector also serves charging.
- `A14:1839:2018` [contradicted] An original invoice is unnecessary when claiming the standard India manufacturer warranty for ClearTrail Plus, provided the buyer says the purchase came from an authorized seller.
- `A14:2019:2198` [contradicted] The stated laboratory playback time for ClearTrail Plus, using a new battery with EQ off at one hundred percent volume, remains 20 hours without any reduction for louder playback.
- `A15:306:495` [unknown] In winter weather below freezing, ClearTrail Mini delivers its full 12-hour laboratory battery duration at fifty percent volume, without the outdoor temperature changing the stated runtime.
- `A15:496:698` [unknown] An authorized India service centre guarantees repair of ClearTrail Mini within two working days after receiving the unit and the required purchase paperwork, regardless of replacement-part availability.
- `A15:700:889` [contradicted] With all port covers closed, ClearTrail Mini is explicitly permitted to be immersed in fresh water, rather than being restricted to the non-immersion use implied by a more cautious reading.
- `A15:890:1074` [contradicted] The manufacturer supports a stereo pair made from one ClearTrail Mini and one ClearTrail Plus, since being members of the same brand is sufficient for cross-model stereo compatibility.
- `A15:1075:1236` [supported] The built-in Wi-Fi capability of ClearTrail Mini is absent, which should be treated as a separate specification from its ability to receive audio over Bluetooth.
- `A15:1433:1627` [unknown] The normal manufacturing origin of ClearTrail Mini is India, even when the unit is purchased through an authorized seller rather than ordered directly from the manufacturer's own retail channel.
- `A15:1628:1825` [unknown] ClearTrail Mini accepts two active Bluetooth source connections at the same time and switches between them automatically, without asking the listener to disconnect one phone before using the other.
- `A15:1827:2026` [supported] Whatever conclusions a buyer draws from the water-resistance rating, water damage remains excluded from the standard India manufacturer warranty covering ClearTrail Mini after an authorized purchase.
- `A15:2027:2174` [supported] For an India purchase at the official catalogue list price on 1 October 2026, ClearTrail Mini costs INR 1,299 including tax but excluding shipping.
- `A15:2175:2354` [contradicted] An original invoice is unnecessary when claiming the standard India manufacturer warranty for ClearTrail Mini, provided the buyer says the purchase came from an authorized seller.
- `A16:306:454` [supported] For an India purchase at the official catalogue list price on 1 October 2026, CloudNote Studio costs INR 2,999 including tax but excluding shipping.
- `A16:455:618` [contradicted] For a current India catalogue comparison before shipping, CloudNote Studio is INR 1,500 less expensive than CloudNote Air, with tax included in both listed prices.
- `A16:620:828` [unknown] The sustained amplifier output of CloudNote Studio is forty watts per channel during ordinary playback, which allows a direct loudness comparison with other speakers advertised using electrical power figures.
- `A16:829:1001` [supported] The move from the 2025 India catalogue to the 2026 catalogue raised the tax-inclusive list price of CloudNote Studio by INR 200, with shipping excluded in both comparisons.
- `A16:1198:1422` [contradicted] Water damage to CloudNote Studio is included in the standard India manufacturer warranty after an authorized purchase, because water resistance should be understood as warranty coverage rather than just a product capability.
- `A16:1423:1613` [unknown] In winter weather below freezing, CloudNote Studio delivers its full 18-hour laboratory battery duration at fifty percent volume, without the outdoor temperature changing the stated runtime.
- `A16:1614:1797` [supported] Considering the speaker alone and leaving retail packaging and accessories out of the measurement, CloudNote Studio has a stated mass of 1.1 kilograms for carrying-weight comparisons.
- `A16:1799:1976` [contradicted] When measuring just the speaker rather than the retail box and accessories, CloudNote Studio weighs 350 grams, matching the carrying-weight figure associated with CloudNote Air.
- `A16:1977:2138` [supported] The official India retail box for CloudNote Studio contains a wall charging adapter, so the box contents should not be inferred just from the charging-port type.
- `A17:335:506` [contradicted] The official India retail box for CloudNote Air includes a wall charging adapter, even though separate accessory lists may make the charging arrangement look less obvious.
- `A17:507:694` [unknown] In winter weather below freezing, CloudNote Air delivers its full 10-hour laboratory battery duration at fifty percent volume, without the outdoor temperature changing the stated runtime.
- `A17:696:879` [contradicted] The manufacturer supports a stereo pair made from one CloudNote Air and one CloudNote Studio, since being members of the same brand is sufficient for cross-model stereo compatibility.
- `A17:880:1054` [supported] Turning CloudNote Air up from fifty to one hundred percent volume in the stated new-battery, EQ-off laboratory tests halves its listed playback time from 10 hours to 5 hours.
- `A17:1055:1247` [unknown] The normal manufacturing origin of CloudNote Air is India, even when the unit is purchased through an authorized seller rather than ordered directly from the manufacturer's own retail channel.
- `A17:1444:1607` [contradicted] For a current India catalogue comparison before shipping, CloudNote Air is INR 1,500 more expensive than CloudNote Studio, with tax included in both listed prices.
- `A17:1608:1785` [unknown] Using a twenty-watt wall adapter, a fully discharged CloudNote Air reaches a complete charge in ninety minutes, so a short charging stop is enough to restore the entire battery.
- `A17:1787:1932` [supported] For an India purchase at the official catalogue list price on 1 October 2026, CloudNote Air costs INR 1,499 including tax but excluding shipping.
- `A17:1933:2114` [supported] Considering the speaker alone and leaving retail packaging and accessories out of the measurement, CloudNote Air has a stated mass of 0.35 kilograms for carrying-weight comparisons.
- `A17:2115:2336` [contradicted] Water damage to CloudNote Air is included in the standard India manufacturer warranty after an authorized purchase, because water resistance should be understood as warranty coverage rather than just a product capability.
- `A17:2338:2519` [unknown] The official India catalogue price of CloudNote Air will drop by INR 300 during January 2027, with that future reduction applying before shipping to purchases from the brand itself.
- `A18:324:490` [supported] The official India retail box for StoneWave Max does not contain a wall charging adapter, so the box contents should not be inferred just from the charging-port type.
- `A18:491:661` [unknown] Orders for StoneWave Max receive free delivery to every India postal code, so there is no separate shipping charge even when a customer selects a remote delivery address.
- `A18:663:840` [contradicted] In the 2025 India catalogue, before the current-year revision, StoneWave Max already carried the same tax-inclusive list price of INR 3,499, excluding shipping from that amount.
- `A18:943:1138` [unknown] StoneWave Max accepts two active Bluetooth source connections at the same time and switches between them automatically, without asking the listener to disconnect one phone before using the other.
- `A18:1335:1518` [contradicted] With all port covers closed, StoneWave Max is permitted to remain immersed in fresh water at a depth of one metre for a full hour under the manufacturer's stated laboratory allowance.
- `A18:1519:1691` [supported] For wired digital audio specifically, the USB-C connector on StoneWave Max does provide an audio-input path, regardless of the fact that the connector also serves charging.
- `A18:1693:1874` [unknown] The official India catalogue price of StoneWave Max will drop by INR 300 during January 2027, with that future reduction applying before shipping to purchases from the brand itself.
- `A18:1875:2044` [contradicted] The built-in microphone is not included on StoneWave Max, without needing an accessory to change the hardware specification being described for this exact speaker model.
- `A19:371:555` [contradicted] For an authorized India purchase with the original invoice and a manufacturing defect, StoneWave Max receives a standard manufacturer warranty lasting 24 months from the purchase date.
- `A19:556:729` [contradicted] When measuring just the speaker rather than the retail box and accessories, StoneWave Max weighs 440 grams, matching the carrying-weight figure associated with StoneWave Go.
- `A19:731:902` [contradicted] The official India retail box for StoneWave Max includes a wall charging adapter, even though separate accessory lists may make the charging arrangement look less obvious.
- `A19:903:1067` [supported] With all port covers closed, the laboratory immersion allowance for StoneWave Max is limited to fresh water at no more than one metre for no more than half an hour.
- `A19:1068:1268` [unknown] No version of StoneWave Max has ever been offered in blue, including previous-year retail stock and editions supplied only through independent authorized sellers rather than the official online store.
- `A19:1465:1654` [unknown] After an announced firmware update next quarter, StoneWave Max will gain a built-in voice assistant that can answer spoken questions without requiring a paired phone to process the request.
- `A19:1655:1832` [contradicted] An original invoice is unnecessary when claiming the standard India manufacturer warranty for StoneWave Max, provided the buyer says the purchase came from an authorized seller.
- `A19:1834:2008` [supported] For manufacturing defects following an authorized India purchase with the original invoice, the standard manufacturer warranty on StoneWave Max lasts 1.5 years from purchase.
- `A19:2009:2201` [unknown] The Bluetooth connection on StoneWave Max maintains uninterrupted playback at a distance of one hundred metres outdoors, even when a listener changes the phone used as the transmitting device.
- `A19:2202:2372` [unknown] Orders for StoneWave Max receive free delivery to every India postal code, so there is no separate shipping charge even when a customer selects a remote delivery address.
- `A20:306:485` [contradicted] The manufacturer supports a stereo pair made from one StoneWave Go and one StoneWave Max, since being members of the same brand is sufficient for cross-model stereo compatibility.
- `A20:486:662` [contradicted] In the 2025 India catalogue, before the current-year revision, StoneWave Go already carried the same tax-inclusive list price of INR 1,999, excluding shipping from that amount.
- `A20:664:855` [unknown] The normal manufacturing origin of StoneWave Go is India, even when the unit is purchased through an authorized seller rather than ordered directly from the manufacturer's own retail channel.
- `A20:856:1046` [supported] The manufacturer permits stereo pairing only between two units of the exact StoneWave Go model, rather than treating every speaker sharing the same brand name as a compatible stereo partner.
- `A20:1243:1434` [unknown] The Bluetooth connection on StoneWave Go maintains uninterrupted playback at a distance of one hundred metres outdoors, even when a listener changes the phone used as the transmitting device.
- `A20:1435:1607` [supported] Despite the declared IPX5 water-resistance rating, the manufacturer does not permit fresh-water immersion of StoneWave Go, even with all of the port covers properly closed.
- `A20:1608:1752` [supported] For an India purchase at the official catalogue list price on 1 October 2026, StoneWave Go costs INR 1,999 including tax but excluding shipping.
- `A20:1754:1949` [unknown] The plastic used in the enclosure of StoneWave Go contains at least sixty percent post-consumer recycled material by weight, excluding the electronic components and the external retail packaging.
- `A21:335:558` [contradicted] Water damage to ClearTrail Plus is included in the standard India manufacturer warranty after an authorized purchase, because water resistance should be understood as warranty coverage rather than just a product capability.
- `A21:559:722` [contradicted] At fifty percent volume with EQ off and a new battery in the laboratory, ClearTrail Plus is rated for 1260 minutes of playback before recharging becomes necessary.
- `A21:724:892` [supported] The official India retail box for ClearTrail Plus does not contain a wall charging adapter, so the box contents should not be inferred just from the charging-port type.
- `A21:893:1087` [unknown] The normal manufacturing origin of ClearTrail Plus is India, even when the unit is purchased through an authorized seller rather than ordered directly from the manufacturer's own retail channel.
- `A21:1284:1478` [unknown] The Bluetooth connection on ClearTrail Plus maintains uninterrupted playback at a distance of one hundred metres outdoors, even when a listener changes the phone used as the transmitting device.
- `A21:1479:1676` [unknown] ClearTrail Plus accepts two active Bluetooth source connections at the same time and switches between them automatically, without asking the listener to disconnect one phone before using the other.
- `A21:1677:1848` [supported] The move from the 2025 India catalogue to the 2026 catalogue raised the tax-inclusive list price of ClearTrail Plus by INR 300, with shipping excluded in both comparisons.
- `A21:1850:2028` [contradicted] When measuring just the speaker rather than the retail box and accessories, ClearTrail Plus weighs 320 grams, matching the carrying-weight figure associated with ClearTrail Mini.
- `A22:324:503` [contradicted] The stated laboratory playback time for ClearTrail Mini, using a new battery with EQ off at one hundred percent volume, remains 12 hours without any reduction for louder playback.
- `A22:504:666` [contradicted] At fifty percent volume with EQ off and a new battery in the laboratory, ClearTrail Mini is rated for 780 minutes of playback before recharging becomes necessary.
- `A22:668:843` [supported] Despite the declared IPX4 water-resistance rating, the manufacturer does not permit fresh-water immersion of ClearTrail Mini, even with all of the port covers properly closed.
- `A22:844:1033` [unknown] In winter weather below freezing, ClearTrail Mini delivers its full 12-hour laboratory battery duration at fifty percent volume, without the outdoor temperature changing the stated runtime.
- `A22:1034:1201` [contradicted] The built-in microphone is included on ClearTrail Mini, without needing an accessory to change the hardware specification being described for this exact speaker model.
- `A22:1398:1552` [supported] For the current India catalogue, ClearTrail Mini is listed at INR 1,200 less than ClearTrail Plus, comparing the two tax-inclusive prices before shipping.
- `A22:1553:1704` [contradicted] For an India purchase at the official catalogue list price on 1 October 2026, ClearTrail Mini still costs INR 999 including tax but excluding shipping.
- `A22:1706:1892` [unknown] ClearTrail Mini supports the AAC Bluetooth audio codec on compatible phones, so its published Bluetooth version can be treated as evidence for that specific audio-compression capability.
- `A22:1893:2087` [unknown] The Bluetooth connection on ClearTrail Mini maintains uninterrupted playback at a distance of one hundred metres outdoors, even when a listener changes the phone used as the transmitting device.
- `A22:2088:2271` [unknown] An opened ClearTrail Mini can be returned to any authorized India seller within thirty days for a full refund, even when the speaker has no manufacturing defect or functional problem.
- `A23:371:548` [contradicted] When measuring just the speaker rather than the retail box and accessories, CloudNote Studio weighs 350 grams, matching the carrying-weight figure associated with CloudNote Air.
- `A23:549:744` [unknown] The Bluetooth connection on CloudNote Studio maintains uninterrupted playback at a distance of one hundred metres outdoors, even when a listener changes the phone used as the transmitting device.
- `A23:746:907` [supported] The official India retail box for CloudNote Studio contains a wall charging adapter, so the box contents should not be inferred just from the charging-port type.
- `A23:908:1098` [unknown] In winter weather below freezing, CloudNote Studio delivers its full 18-hour laboratory battery duration at fifty percent volume, without the outdoor temperature changing the stated runtime.
- `A23:1295:1477` [contradicted] The official India retail box for CloudNote Studio does not include a wall charging adapter, even though separate accessory lists may make the charging arrangement look less obvious.
- `A23:1478:1662` [unknown] An opened CloudNote Studio can be returned to any authorized India seller within thirty days for a full refund, even when the speaker has no manufacturing defect or functional problem.
- `A23:1663:1854` [supported] Even when other warranty conditions are met for an authorized India purchase, the original purchase invoice is still required to claim the standard manufacturer warranty for CloudNote Studio.
- `A23:1856:2056` [supported] Whatever conclusions a buyer draws from the water-resistance rating, water damage remains excluded from the standard India manufacturer warranty covering CloudNote Studio after an authorized purchase.
- `A24:306:498` [unknown] The Bluetooth connection on CloudNote Air maintains uninterrupted playback at a distance of one hundred metres outdoors, even when a listener changes the phone used as the transmitting device.
- `A24:499:683` [contradicted] For an authorized India purchase with the original invoice and a manufacturing defect, CloudNote Air receives a standard manufacturer warranty lasting 30 months from the purchase date.
- `A24:685:890` [unknown] Compared with the unlisted RivalSound Trek, CloudNote Air provides two additional hours of playback under identical new-battery, fifty-percent-volume, EQ-off laboratory testing conditions for both devices.
- `A24:891:1091` [unknown] An authorized India service centre guarantees repair of CloudNote Air within two working days after receiving the unit and the required purchase paperwork, regardless of replacement-part availability.
- `A24:1092:1287` [unknown] CloudNote Air accepts two active Bluetooth source connections at the same time and switches between them automatically, without asking the listener to disconnect one phone before using the other.
- `A24:1484:1675` [supported] The manufacturer permits stereo pairing only between two units of the exact CloudNote Air model, rather than treating every speaker sharing the same brand name as a compatible stereo partner.
- `A24:1676:1854` [contradicted] When measuring just the speaker rather than the retail box and accessories, CloudNote Air weighs 1100 grams, matching the carrying-weight figure associated with CloudNote Studio.
- `A24:1856:2025` [supported] The move from the 2025 India catalogue to the 2026 catalogue raised the tax-inclusive list price of CloudNote Air by INR 300, with shipping excluded in both comparisons.
- `A24:2026:2214` [supported] Even when other warranty conditions are met for an authorized India purchase, the original purchase invoice is still required to claim the standard manufacturer warranty for CloudNote Air.
- `A24:2215:2381` [supported] The official India retail box for CloudNote Air does not contain a wall charging adapter, so the box contents should not be inferred just from the charging-port type.
- `A25:306:459` [supported] For the current India catalogue, CloudNote Air is listed at INR 1,500 less than CloudNote Studio, comparing the two tax-inclusive prices before shipping.
- `A25:460:630` [unknown] Orders for CloudNote Air receive free delivery to every India postal code, so there is no separate shipping charge even when a customer selects a remote delivery address.
- `A25:632:824` [unknown] The Bluetooth connection on CloudNote Air maintains uninterrupted playback at a distance of one hundred metres outdoors, even when a listener changes the phone used as the transmitting device.
- `A25:825:988` [contradicted] For a current India catalogue comparison before shipping, CloudNote Air is INR 1,500 more expensive than CloudNote Studio, with tax included in both listed prices.
- `A25:1185:1366` [unknown] An opened CloudNote Air can be returned to any authorized India seller within thirty days for a full refund, even when the speaker has no manufacturing defect or functional problem.
- `A25:1367:1526` [supported] The built-in Wi-Fi capability of CloudNote Air is absent, which should be treated as a separate specification from its ability to receive audio over Bluetooth.
- `A25:1527:1672` [supported] For an India purchase at the official catalogue list price on 1 October 2026, CloudNote Air costs INR 1,499 including tax but excluding shipping.
- `A25:1674:1851` [contradicted] An original invoice is unnecessary when claiming the standard India manufacturer warranty for CloudNote Air, provided the buyer says the purchase came from an authorized seller.
- `A25:1852:2023` [contradicted] The official India retail box for CloudNote Air includes a wall charging adapter, even though separate accessory lists may make the charging arrangement look less obvious.
- `A26:335:556` [contradicted] Water damage to StoneWave Max is included in the standard India manufacturer warranty after an authorized purchase, because water resistance should be understood as warranty coverage rather than just a product capability.
- `A26:557:727` [unknown] Orders for StoneWave Max receive free delivery to every India postal code, so there is no separate shipping charge even when a customer selects a remote delivery address.
- `A26:729:925` [unknown] The plastic used in the enclosure of StoneWave Max contains at least sixty percent post-consumer recycled material by weight, excluding the electronic components and the external retail packaging.
- `A26:926:1107` [unknown] The official India catalogue price of StoneWave Max will drop by INR 300 during January 2027, with that future reduction applying before shipping to purchases from the brand itself.
- `A26:1108:1265` [contradicted] The built-in Wi-Fi capability of StoneWave Max is present, independently of whatever Bluetooth connection a listener might also choose for everyday playback.
- `A26:1462:1650` [supported] Even when other warranty conditions are met for an authorized India purchase, the original purchase invoice is still required to claim the standard manufacturer warranty for StoneWave Max.
- `A26:1651:1796` [supported] For an India purchase at the official catalogue list price on 1 October 2026, StoneWave Max costs INR 3,499 including tax but excluding shipping.
- `A26:1798:1975` [contradicted] An original invoice is unnecessary when claiming the standard India manufacturer warranty for StoneWave Max, provided the buyer says the purchase came from an authorized seller.
- `A26:1976:2153` [unknown] Using a twenty-watt wall adapter, a fully discharged StoneWave Max reaches a complete charge in ninety minutes, so a short charging stop is enough to restore the entire battery.
- `A26:2154:2351` [supported] Whatever conclusions a buyer draws from the water-resistance rating, water damage remains excluded from the standard India manufacturer warranty covering StoneWave Max after an authorized purchase.
- `A27:324:493` [unknown] Orders for StoneWave Go receive free delivery to every India postal code, so there is no separate shipping charge even when a customer selects a remote delivery address.
- `A27:494:688` [unknown] StoneWave Go accepts two active Bluetooth source connections at the same time and switches between them automatically, without asking the listener to disconnect one phone before using the other.
- `A27:690:873` [contradicted] Basic Bluetooth playback on StoneWave Go requires the manufacturer companion app to be installed first, rather than allowing a listener to pair a source and start playback without it.
- `A27:874:1033` [contradicted] For a current India catalogue comparison before shipping, StoneWave Go is INR 1,500 more expensive than StoneWave Max, with tax included in both listed prices.
- `A27:1230:1392` [supported] Looking back specifically at the 2025 India catalogue rather than the current offer, the listed tax-inclusive price of StoneWave Go was INR 1,799 before shipping.
- `A27:1393:1579` [contradicted] With all port covers closed, StoneWave Go is explicitly permitted to be immersed in fresh water, rather than being restricted to the non-immersion use implied by a more cautious reading.
- `A27:1580:1745` [supported] The official India retail box for StoneWave Go does not contain a wall charging adapter, so the box contents should not be inferred just from the charging-port type.
- `A27:1747:1938` [unknown] The Bluetooth connection on StoneWave Go maintains uninterrupted playback at a distance of one hundred metres outdoors, even when a listener changes the phone used as the transmitting device.
- `A27:1939:2088` [supported] For the current India catalogue, StoneWave Go is listed at INR 1,500 less than StoneWave Max, comparing the two tax-inclusive prices before shipping.
- `A28:371:548` [supported] Turning ClearTrail Plus up from fifty to one hundred percent volume in the stated new-battery, EQ-off laboratory tests halves its listed playback time from 20 hours to 10 hours.
- `A28:549:751` [unknown] No version of ClearTrail Plus has ever been offered in blue, including previous-year retail stock and editions supplied only through independent authorized sellers rather than the official online store.
- `A28:753:942` [unknown] In winter weather below freezing, ClearTrail Plus delivers its full 20-hour laboratory battery duration at fifty percent volume, without the outdoor temperature changing the stated runtime.
- `A28:943:1122` [contradicted] The stated laboratory playback time for ClearTrail Plus, using a new battery with EQ off at one hundred percent volume, remains 20 hours without any reduction for louder playback.
- `A28:1123:1302` [unknown] Using a twenty-watt wall adapter, a fully discharged ClearTrail Plus reaches a complete charge in ninety minutes, so a short charging stop is enough to restore the entire battery.
- `A28:1499:1671` [unknown] Orders for ClearTrail Plus receive free delivery to every India postal code, so there is no separate shipping charge even when a customer selects a remote delivery address.
- `A28:1672:1819` [supported] For an India purchase at the official catalogue list price on 1 October 2026, ClearTrail Plus costs INR 2,499 including tax but excluding shipping.
- `A28:1821:2006` [contradicted] With all port covers closed, ClearTrail Plus is permitted to remain immersed in fresh water at a depth of one metre for a full hour under the manufacturer's stated laboratory allowance.
- `A28:2007:2180` [contradicted] The official India retail box for ClearTrail Plus includes a wall charging adapter, even though separate accessory lists may make the charging arrangement look less obvious.
- `A28:2181:2355` [supported] The built-in microphone is included on ClearTrail Plus, so microphone availability should be checked for this exact model instead of copied from another speaker in the range.
- `A29:306:453` [supported] For an India purchase at the official catalogue list price on 1 October 2026, ClearTrail Mini costs INR 1,299 including tax but excluding shipping.
- `A29:454:615` [supported] The built-in Wi-Fi capability of ClearTrail Mini is absent, which should be treated as a separate specification from its ability to receive audio over Bluetooth.
- `A29:617:788` [supported] The move from the 2025 India catalogue to the 2026 catalogue raised the tax-inclusive list price of ClearTrail Mini by INR 300, with shipping excluded in both comparisons.
- `A29:789:975` [unknown] ClearTrail Mini supports the AAC Bluetooth audio codec on compatible phones, so its published Bluetooth version can be treated as evidence for that specific audio-compression capability.
- `A29:1172:1369` [unknown] ClearTrail Mini accepts two active Bluetooth source connections at the same time and switches between them automatically, without asking the listener to disconnect one phone before using the other.
- `A29:1370:1549` [contradicted] An original invoice is unnecessary when claiming the standard India manufacturer warranty for ClearTrail Mini, provided the buyer says the purchase came from an authorized seller.
- `A29:1550:1701` [contradicted] For an India purchase at the official catalogue list price on 1 October 2026, ClearTrail Mini still costs INR 999 including tax but excluding shipping.
- `A29:1703:1882` [contradicted] In the 2025 India catalogue, before the current-year revision, ClearTrail Mini already carried the same tax-inclusive list price of INR 1,299, excluding shipping from that amount.
- `A29:1883:2066` [supported] With a new battery, EQ disabled and volume held at fifty percent in the laboratory, ClearTrail Mini has a stated playback duration of 720 minutes under those specific test conditions.
- `A30:306:509` [unknown] No version of CloudNote Studio has ever been offered in blue, including previous-year retail stock and editions supplied only through independent authorized sellers rather than the official online store.
- `A30:510:676` [supported] Looking back specifically at the 2025 India catalogue rather than the current offer, the listed tax-inclusive price of CloudNote Studio was INR 2,799 before shipping.
- `A30:678:860` [contradicted] The official India retail box for CloudNote Studio does not include a wall charging adapter, even though separate accessory lists may make the charging arrangement look less obvious.
- `A30:861:1061` [supported] Whatever conclusions a buyer draws from the water-resistance rating, water damage remains excluded from the standard India manufacturer warranty covering CloudNote Studio after an authorized purchase.
- `A30:1062:1242` [contradicted] In the 2025 India catalogue, before the current-year revision, CloudNote Studio already carried the same tax-inclusive list price of INR 2,999, excluding shipping from that amount.
- `A30:1439:1663` [contradicted] Water damage to CloudNote Studio is included in the standard India manufacturer warranty after an authorized purchase, because water resistance should be understood as warranty coverage rather than just a product capability.
- `A30:1664:1844` [contradicted] An original invoice is unnecessary when claiming the standard India manufacturer warranty for CloudNote Studio, provided the buyer says the purchase came from an authorized seller.
- `A30:1846:2030` [unknown] The official India catalogue price of CloudNote Studio will drop by INR 300 during January 2027, with that future reduction applying before shipping to purchases from the brand itself.
- `A30:2031:2229` [unknown] CloudNote Studio accepts two active Bluetooth source connections at the same time and switches between them automatically, without asking the listener to disconnect one phone before using the other.
- `A30:2230:2417` [unknown] CloudNote Studio supports the AAC Bluetooth audio codec on compatible phones, so its published Bluetooth version can be treated as evidence for that specific audio-compression capability.
- `A30:2419:2572` [supported] For the current India catalogue, CloudNote Studio is listed at INR 1,500 more than CloudNote Air, comparing the two tax-inclusive prices before shipping.
- `A31:324:477` [supported] For the current India catalogue, CloudNote Studio is listed at INR 1,500 more than CloudNote Air, comparing the two tax-inclusive prices before shipping.
- `A31:478:653` [supported] For wired digital audio specifically, the USB-C connector on CloudNote Studio does provide an audio-input path, regardless of the fact that the connector also serves charging.
- `A31:655:854` [unknown] The plastic used in the enclosure of CloudNote Studio contains at least sixty percent post-consumer recycled material by weight, excluding the electronic components and the external retail packaging.
- `A31:855:1050` [unknown] The normal manufacturing origin of CloudNote Studio is India, even when the unit is purchased through an authorized seller rather than ordered directly from the manufacturer's own retail channel.
- `A31:1051:1238` [unknown] CloudNote Studio supports the AAC Bluetooth audio codec on compatible phones, so its published Bluetooth version can be treated as evidence for that specific audio-compression capability.
- `A31:1435:1615` [contradicted] An original invoice is unnecessary when claiming the standard India manufacturer warranty for CloudNote Studio, provided the buyer says the purchase came from an authorized seller.
- `A31:1616:1793` [contradicted] When measuring just the speaker rather than the retail box and accessories, CloudNote Studio weighs 350 grams, matching the carrying-weight figure associated with CloudNote Air.
- `A31:1795:1963` [contradicted] The built-in microphone is included on CloudNote Studio, without needing an accessory to change the hardware specification being described for this exact speaker model.
- `A31:1964:2155` [supported] Even when other warranty conditions are met for an authorized India purchase, the original purchase invoice is still required to claim the standard manufacturer warranty for CloudNote Studio.
- `A31:2156:2351` [unknown] The Bluetooth connection on CloudNote Studio maintains uninterrupted playback at a distance of one hundred metres outdoors, even when a listener changes the phone used as the transmitting device.
- `A32:371:576` [unknown] The sustained amplifier output of CloudNote Air is forty watts per channel during ordinary playback, which allows a direct loudness comparison with other speakers advertised using electrical power figures.
- `A32:577:749` [supported] The built-in microphone is included on CloudNote Air, so microphone availability should be checked for this exact model instead of copied from another speaker in the range.
- `A32:751:928` [contradicted] In the 2025 India catalogue, before the current-year revision, CloudNote Air already carried the same tax-inclusive list price of INR 1,499, excluding shipping from that amount.
- `A32:1031:1205` [supported] Turning CloudNote Air up from fifty to one hundred percent volume in the stated new-battery, EQ-off laboratory tests halves its listed playback time from 10 hours to 5 hours.
- `A32:1402:1583` [supported] Considering the speaker alone and leaving retail packaging and accessories out of the measurement, CloudNote Air has a stated mass of 0.35 kilograms for carrying-weight comparisons.
- `A32:1584:1771` [contradicted] With all port covers closed, CloudNote Air is explicitly permitted to be immersed in fresh water, rather than being restricted to the non-immersion use implied by a more cautious reading.
- `A32:1773:1960` [unknown] In winter weather below freezing, CloudNote Air delivers its full 10-hour laboratory battery duration at fifty percent volume, without the outdoor temperature changing the stated runtime.
- `A32:1961:2134` [supported] Despite the declared IPX4 water-resistance rating, the manufacturer does not permit fresh-water immersion of CloudNote Air, even with all of the port covers properly closed.
- `A32:2135:2319` [contradicted] Basic Bluetooth playback on CloudNote Air requires the manufacturer companion app to be installed first, rather than allowing a listener to pair a source and start playback without it.
- `A33:306:498` [unknown] The Bluetooth connection on StoneWave Max maintains uninterrupted playback at a distance of one hundred metres outdoors, even when a listener changes the phone used as the transmitting device.
- `A33:499:656` [contradicted] The built-in Wi-Fi capability of StoneWave Max is present, independently of whatever Bluetooth connection a listener might also choose for everyday playback.
- `A33:658:842` [contradicted] For an authorized India purchase with the original invoice and a manufacturing defect, StoneWave Max receives a standard manufacturer warranty lasting 24 months from the purchase date.
- `A33:843:1027` [contradicted] Basic Bluetooth playback on StoneWave Max requires the manufacturer companion app to be installed first, rather than allowing a listener to pair a source and start playback without it.
- `A33:1028:1203` [supported] Turning StoneWave Max up from fifty to one hundred percent volume in the stated new-battery, EQ-off laboratory tests halves its listed playback time from 24 hours to 12 hours.
- `A33:1400:1574` [supported] For manufacturing defects following an authorized India purchase with the original invoice, the standard manufacturer warranty on StoneWave Max lasts 1.5 years from purchase.
- `A33:1575:1780` [unknown] The sustained amplifier output of StoneWave Max is forty watts per channel during ordinary playback, which allows a direct loudness comparison with other speakers advertised using electrical power figures.
- `A33:1782:1951` [contradicted] The built-in microphone is not included on StoneWave Max, without needing an accessory to change the hardware specification being described for this exact speaker model.
- `A33:1952:2111` [supported] The built-in Wi-Fi capability of StoneWave Max is absent, which should be treated as a separate specification from its ability to receive audio over Bluetooth.
- `A33:2112:2307` [unknown] StoneWave Max accepts two active Bluetooth source connections at the same time and switches between them automatically, without asking the listener to disconnect one phone before using the other.
- `A33:2309:2509` [unknown] No version of StoneWave Max has ever been offered in blue, including previous-year retail stock and editions supplied only through independent authorized sellers rather than the official online store.
- `A34:306:479` [supported] Turning StoneWave Go up from fifty to one hundred percent volume in the stated new-battery, EQ-off laboratory tests halves its listed playback time from 16 hours to 8 hours.
- `A34:480:656` [contradicted] An original invoice is unnecessary when claiming the standard India manufacturer warranty for StoneWave Go, provided the buyer says the purchase came from an authorized seller.
- `A34:658:808` [contradicted] For an India purchase at the official catalogue list price on 1 October 2026, StoneWave Go still costs INR 1,799 including tax but excluding shipping.
- `A34:809:958` [supported] For the current India catalogue, StoneWave Go is listed at INR 1,500 less than StoneWave Max, comparing the two tax-inclusive prices before shipping.
- `A34:1155:1315` [contradicted] At fifty percent volume with EQ off and a new battery in the laboratory, StoneWave Go is rated for 1020 minutes of playback before recharging becomes necessary.
- `A34:1316:1496` [unknown] The official India catalogue price of StoneWave Go will drop by INR 300 during January 2027, with that future reduction applying before shipping to purchases from the brand itself.
- `A34:1497:1683` [unknown] In winter weather below freezing, StoneWave Go delivers its full 16-hour laboratory battery duration at fifty percent volume, without the outdoor temperature changing the stated runtime.
- `A34:1685:1854` [unknown] Orders for StoneWave Go receive free delivery to every India postal code, so there is no separate shipping charge even when a customer selects a remote delivery address.
- `A35:335:520` [contradicted] With all port covers closed, ClearTrail Plus is permitted to remain immersed in fresh water at a depth of one metre for a full hour under the manufacturer's stated laboratory allowance.
- `A35:521:687` [supported] With all port covers closed, the laboratory immersion allowance for ClearTrail Plus is limited to fresh water at no more than one metre for no more than half an hour.
- `A35:689:883` [unknown] The Bluetooth connection on ClearTrail Plus maintains uninterrupted playback at a distance of one hundred metres outdoors, even when a listener changes the phone used as the transmitting device.
- `A35:884:1070` [unknown] ClearTrail Plus supports the AAC Bluetooth audio codec on compatible phones, so its published Bluetooth version can be treated as evidence for that specific audio-compression capability.
- `A35:1071:1245` [supported] For manufacturing defects following an authorized India purchase with the original invoice, the standard manufacturer warranty on ClearTrail Plus lasts 1 years from purchase.
- `A35:1442:1606` [contradicted] For a current India catalogue comparison before shipping, ClearTrail Plus is INR 1,200 less expensive than ClearTrail Mini, with tax included in both listed prices.
- `A35:1607:1804` [unknown] ClearTrail Plus accepts two active Bluetooth source connections at the same time and switches between them automatically, without asking the listener to disconnect one phone before using the other.
- `A35:1806:1969` [contradicted] At fifty percent volume with EQ off and a new battery in the laboratory, ClearTrail Plus is rated for 1260 minutes of playback before recharging becomes necessary.
- `A35:1970:2129` [contradicted] The built-in Wi-Fi capability of ClearTrail Plus is present, independently of whatever Bluetooth connection a listener might also choose for everyday playback.
- `A35:2130:2321` [unknown] After an announced firmware update next quarter, ClearTrail Plus will gain a built-in voice assistant that can answer spoken questions without requiring a paired phone to process the request.
- `A36:324:496` [unknown] Orders for ClearTrail Mini receive free delivery to every India postal code, so there is no separate shipping charge even when a customer selects a remote delivery address.
- `A36:497:687` [supported] Even when other warranty conditions are met for an authorized India purchase, the original purchase invoice is still required to claim the standard manufacturer warranty for ClearTrail Mini.
- `A36:689:891` [unknown] An authorized India service centre guarantees repair of ClearTrail Mini within two working days after receiving the unit and the required purchase paperwork, regardless of replacement-part availability.
- `A36:892:1059` [contradicted] The built-in microphone is included on ClearTrail Mini, without needing an accessory to change the hardware specification being described for this exact speaker model.
- `A36:1256:1463` [unknown] Compared with the unlisted RivalSound Trek, ClearTrail Mini provides two additional hours of playback under identical new-battery, fifty-percent-volume, EQ-off laboratory testing conditions for both devices.
- `A36:1464:1650` [contradicted] For an authorized India purchase with the original invoice and a manufacturing defect, ClearTrail Mini receives a standard manufacturer warranty lasting 18 months from the purchase date.
- `A36:1651:1822` [supported] The move from the 2025 India catalogue to the 2026 catalogue raised the tax-inclusive list price of ClearTrail Mini by INR 300, with shipping excluded in both comparisons.
- `A36:1824:1978` [supported] For the current India catalogue, ClearTrail Mini is listed at INR 1,200 less than ClearTrail Plus, comparing the two tax-inclusive prices before shipping.
- `A37:371:556` [supported] Basic Bluetooth listening on ClearTrail Mini does not require the manufacturer companion app to be installed, even if a buyer is interested in optional app-related features or settings.
- `A37:557:736` [contradicted] The stated laboratory playback time for ClearTrail Mini, using a new battery with EQ off at one hundred percent volume, remains 12 hours without any reduction for louder playback.
- `A37:738:917` [unknown] Using a twenty-watt wall adapter, a fully discharged ClearTrail Mini reaches a complete charge in ninety minutes, so a short charging stop is enough to restore the entire battery.
- `A37:918:1096` [supported] The built-in microphone is not included on ClearTrail Mini, so microphone availability should be checked for this exact model instead of copied from another speaker in the range.
- `A37:1097:1275` [supported] For wired digital audio specifically, the USB-C connector on ClearTrail Mini does not provide an audio-input path, regardless of the fact that the connector also serves charging.
- `A37:1472:1658` [contradicted] For an authorized India purchase with the original invoice and a manufacturing defect, ClearTrail Mini receives a standard manufacturer warranty lasting 18 months from the purchase date.
- `A37:1659:1853` [unknown] The normal manufacturing origin of ClearTrail Mini is India, even when the unit is purchased through an authorized seller rather than ordered directly from the manufacturer's own retail channel.
- `A37:1855:2009` [supported] For the current India catalogue, ClearTrail Mini is listed at INR 1,200 less than ClearTrail Plus, comparing the two tax-inclusive prices before shipping.
- `A37:2010:2217` [unknown] The sustained amplifier output of ClearTrail Mini is forty watts per channel during ordinary playback, which allows a direct loudness comparison with other speakers advertised using electrical power figures.
- `A37:2218:2407` [unknown] In winter weather below freezing, ClearTrail Mini delivers its full 12-hour laboratory battery duration at fifty percent volume, without the outdoor temperature changing the stated runtime.
- `A38:306:486` [contradicted] An original invoice is unnecessary when claiming the standard India manufacturer warranty for CloudNote Studio, provided the buyer says the purchase came from an authorized seller.
- `A38:487:662` [supported] For manufacturing defects following an authorized India purchase with the original invoice, the standard manufacturer warranty on CloudNote Studio lasts 2 years from purchase.
- `A38:664:843` [supported] The built-in microphone is not included on CloudNote Studio, so microphone availability should be checked for this exact model instead of copied from another speaker in the range.
- `A38:844:1011` [supported] With all port covers closed, the laboratory immersion allowance for CloudNote Studio is limited to fresh water at no more than one metre for no more than half an hour.
- `A38:1208:1388` [unknown] Using a twenty-watt wall adapter, a fully discharged CloudNote Studio reaches a complete charge in ninety minutes, so a short charging stop is enough to restore the entire battery.
- `A38:1389:1592` [unknown] No version of CloudNote Studio has ever been offered in blue, including previous-year retail stock and editions supplied only through independent authorized sellers rather than the official online store.
- `A38:1593:1792` [unknown] The plastic used in the enclosure of CloudNote Studio contains at least sixty percent post-consumer recycled material by weight, excluding the electronic components and the external retail packaging.
- `A38:1794:1977` [contradicted] The manufacturer supports a stereo pair made from one CloudNote Studio and one CloudNote Air, since being members of the same brand is sufficient for cross-model stereo compatibility.
- `A38:1978:2164` [contradicted] With all port covers closed, CloudNote Studio is permitted to remain immersed in fresh water at a depth of one metre for a full hour under the manufacturer's stated laboratory allowance.
- `A39:306:493` [contradicted] With all port covers closed, CloudNote Air is explicitly permitted to be immersed in fresh water, rather than being restricted to the non-immersion use implied by a more cautious reading.
- `A39:494:691` [supported] Whatever conclusions a buyer draws from the water-resistance rating, water damage remains excluded from the standard India manufacturer warranty covering CloudNote Air after an authorized purchase.
- `A39:693:869` [supported] For wired digital audio specifically, the USB-C connector on CloudNote Air does not provide an audio-input path, regardless of the fact that the connector also serves charging.
- `A39:870:1062` [unknown] The Bluetooth connection on CloudNote Air maintains uninterrupted playback at a distance of one hundred metres outdoors, even when a listener changes the phone used as the transmitting device.
- `A39:1063:1245` [contradicted] For wired digital audio specifically, the USB-C connector on CloudNote Air does provide an audio-input path, so the connector can be treated accordingly when choosing a wired source.
- `A39:1442:1614` [supported] The built-in microphone is included on CloudNote Air, so microphone availability should be checked for this exact model instead of copied from another speaker in the range.
- `A39:1615:1792` [contradicted] An original invoice is unnecessary when claiming the standard India manufacturer warranty for CloudNote Air, provided the buyer says the purchase came from an authorized seller.
- `A39:1794:1971` [unknown] Using a twenty-watt wall adapter, a fully discharged CloudNote Air reaches a complete charge in ninety minutes, so a short charging stop is enough to restore the entire battery.
- `A39:1972:2172` [unknown] An authorized India service centre guarantees repair of CloudNote Air within two working days after receiving the unit and the required purchase paperwork, regardless of replacement-part availability.
- `A39:2173:2360` [unknown] In winter weather below freezing, CloudNote Air delivers its full 10-hour laboratory battery duration at fifty percent volume, without the outdoor temperature changing the stated runtime.
- `A40:335:512` [contradicted] In the 2025 India catalogue, before the current-year revision, StoneWave Max already carried the same tax-inclusive list price of INR 3,499, excluding shipping from that amount.
- `A40:513:677` [supported] With all port covers closed, the laboratory immersion allowance for StoneWave Max is limited to fresh water at no more than one metre for no more than half an hour.
- `A40:679:871` [unknown] The Bluetooth connection on StoneWave Max maintains uninterrupted playback at a distance of one hundred metres outdoors, even when a listener changes the phone used as the transmitting device.
- `A40:872:1041` [supported] The move from the 2025 India catalogue to the 2026 catalogue raised the tax-inclusive list price of StoneWave Max by INR 200, with shipping excluded in both comparisons.
- `A40:1238:1422` [unknown] StoneWave Max supports the AAC Bluetooth audio codec on compatible phones, so its published Bluetooth version can be treated as evidence for that specific audio-compression capability.
- `A40:1423:1572` [supported] For the current India catalogue, StoneWave Max is listed at INR 1,500 more than StoneWave Go, comparing the two tax-inclusive prices before shipping.
- `A40:1573:1776` [unknown] A retail purchase of StoneWave Max in Germany qualifies for the same 18-month manufacturer warranty described for authorized India purchases, without any different regional terms affecting that duration.
- `A40:1778:1947` [contradicted] The built-in microphone is not included on StoneWave Max, without needing an accessory to change the hardware specification being described for this exact speaker model.
- `A40:1948:2134` [contradicted] For wired digital audio specifically, the USB-C connector on StoneWave Max does not provide an audio-input path, so the connector can be treated accordingly when choosing a wired source.

## Extra (unmatched) predictions


## Wrong labels


## Answer outcomes

| answer | status | claims | turns | latency ms | error |
|---|---|---|---|---|---|
| A01 | error | 0 | 1 | 815 | provider_error provider returned HTTP 404 |
| A02 | error | 0 | 1 | 421 | provider_error provider returned HTTP 404 |
| A03 | error | 0 | 1 | 818 | provider_error provider returned HTTP 404 |
| A04 | error | 0 | 1 | 524 | provider_error provider returned HTTP 404 |
| A05 | error | 0 | 1 | 819 | provider_error provider returned HTTP 404 |
| A06 | error | 0 | 1 | 536 | provider_error provider returned HTTP 404 |
| A07 | error | 0 | 1 | 820 | provider_error provider returned HTTP 404 |
| A08 | error | 0 | 1 | 533 | provider_error provider returned HTTP 404 |
| A09 | error | 0 | 1 | 528 | provider_error provider returned HTTP 404 |
| A10 | error | 0 | 1 | 543 | provider_error provider returned HTTP 404 |
| A11 | error | 0 | 1 | 406 | provider_error provider returned HTTP 404 |
| A12 | error | 0 | 1 | 392 | provider_error provider returned HTTP 404 |
| A13 | error | 0 | 1 | 384 | provider_error provider returned HTTP 404 |
| A14 | error | 0 | 1 | 377 | provider_error provider returned HTTP 404 |
| A15 | error | 0 | 1 | 382 | provider_error provider returned HTTP 404 |
| A16 | error | 0 | 1 | 375 | provider_error provider returned HTTP 404 |
| A17 | error | 0 | 1 | 390 | provider_error provider returned HTTP 404 |
| A18 | error | 0 | 1 | 407 | provider_error provider returned HTTP 404 |
| A19 | error | 0 | 1 | 414 | provider_error provider returned HTTP 404 |
| A20 | error | 0 | 1 | 396 | provider_error provider returned HTTP 404 |
| A21 | error | 0 | 1 | 385 | provider_error provider returned HTTP 404 |
| A22 | error | 0 | 1 | 409 | provider_error provider returned HTTP 404 |
| A23 | error | 0 | 1 | 404 | provider_error provider returned HTTP 404 |
| A24 | error | 0 | 1 | 411 | provider_error provider returned HTTP 404 |
| A25 | error | 0 | 1 | 397 | provider_error provider returned HTTP 404 |
| A26 | error | 0 | 1 | 413 | provider_error provider returned HTTP 404 |
| A27 | error | 0 | 1 | 398 | provider_error provider returned HTTP 404 |
| A28 | error | 0 | 1 | 389 | provider_error provider returned HTTP 404 |
| A29 | error | 0 | 1 | 390 | provider_error provider returned HTTP 404 |
| A30 | error | 0 | 1 | 410 | provider_error provider returned HTTP 404 |
| A31 | error | 0 | 1 | 370 | provider_error provider returned HTTP 404 |
| A32 | error | 0 | 1 | 554 | provider_error provider returned HTTP 404 |
| A33 | error | 0 | 1 | 395 | provider_error provider returned HTTP 404 |
| A34 | error | 0 | 1 | 381 | provider_error provider returned HTTP 404 |
| A35 | error | 0 | 1 | 375 | provider_error provider returned HTTP 404 |
| A36 | error | 0 | 1 | 368 | provider_error provider returned HTTP 404 |
| A37 | error | 0 | 1 | 385 | provider_error provider returned HTTP 404 |
| A38 | error | 0 | 1 | 395 | provider_error provider returned HTTP 404 |
| A39 | error | 0 | 1 | 384 | provider_error provider returned HTTP 404 |
| A40 | error | 0 | 1 | 383 | provider_error provider returned HTTP 404 |

## Predictions


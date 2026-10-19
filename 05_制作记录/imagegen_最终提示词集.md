# 《推光》imagegen最终提示词集 · v2

内置imagegen；29张入选图的实际提示词和引用图如下。全部35次生成及退回过程保留在imagegen_生成记录.jsonl；源图为AI创作参考，不是工坊实拍。

## W01_workshop.png

编号：W01；工坊空间母图；实际尺寸：1672×941。

输入参考：无，文字生成。

```text
Use case: photorealistic-natural. Asset type: single production reference photograph for a restrained, realistic contemporary Chinese lacquer craft film, W01 environment master. Create ONE clean landscape 16:9 photograph, no collage, no labels or text. An ordinary small actively used contemporary Pingyao lacquer workshop, not a museum or ancient fantasy: plain light gray plaster walls, a dark brown solid wood rectangular workbench across the foreground, a landscape rectangular charcoal-gray non-slip work mat centered on the bench. A simple wooden grid window is on the LEFT wall, with only two columns and three rows of panes, admitting controlled soft daylight from the left. Modest weak ambient fill, deep but readable shadows. At back right a plain brown wooden drying/storage cabinet with shelves and simple doors; one door slightly ajar, cabinet interior dim and dry, not lit by direct sun. A few unobtrusive practical hand tools at the far edge of the bench, no clutter, no identifiable logos. No person and NO lacquer board on the mat yet; the empty pad provides the consistent place for a 30 by 20 cm board in subsequent assets. Camera near operator height, slightly above the bench, three-quarter wide view; bench foreground and left window spatial relation clearly visible, natural straight perspective. Neutral blacks, soft gray, dark brown; quiet contemporary documentary realism, believable wood grain and subtle working wear. No floating dust, haze, smoke, incense, red lanterns, elaborate antique decoration, fake historic garments, gold particles, heavy film grain, lens flare, overexposure, typography or watermark.
```

## H01_hands_master.png

编号：H01；双手与灰袖口母图；实际尺寸：1536×1024。

输入参考：无，文字生成。

```text
Use case: photorealistic-natural. Asset type: H01 anonymous artisan hands identity reference, ONE single photorealistic image, not a multi-panel sheet. Landscape 3:2 photograph of the SAME person's two hands with light gray cotton work-shirt cuffs, resting naturally palm-down on a plain charcoal gray work mat. Both hands fully visible, left hand on the image left, right hand on the image right, wrists enter from bottom edge like an operator looking down. Anonymous adult aged about 25-35, natural medium-light warm East Asian skin, clean short nails, no jewelry, no watch, no tattoos, no extra identifying marks; realistic pores and gentle knuckles, calm working hands, not cosmetically manicured and not heavily aged. Loose simple light gray cotton sleeves end near the wrists, identical cuff construction on both hands. Soft controlled daylight from LEFT, weak fill, neutral quiet realistic color, subtle fabric weave. All five fingers of each hand anatomically correct and clearly separated, thumbs on anatomically correct sides. No extra limbs, no missing/fused fingers, no black lacquer stains, no redness, injury, sweat, tool, object, text, numbers, grid, logos or watermark. No face or body above forearms. This is the master for later right-hand, left-hand, and clothed torso variants.
```

## H01_right_hand.png

编号：H01；右手独立参考；实际尺寸：1536×1024。

输入参考：02_视觉资产/H01_hands_master.png

```text
Use case: identity-preserve. Input is the H01 SAME PERSON hand identity master. Make ONE photorealistic standalone reference photograph of only the anatomical RIGHT HAND that is on the RIGHT HALF of the input. Preserve this exact hand's skin tone, nail shapes, finger proportions, natural knuckles and the same light-gray cotton cuff construction. Remove the other hand. Center the single right hand palm-down on the same charcoal-gray mat, wrist enters from bottom edge, all FIVE fingers fully visible with natural relaxed separation; in this top-down hand-back view the RIGHT THUMB is on IMAGE LEFT. Do not mirror a left hand. Same soft left daylight and natural exposure. No jewelry, no watch, no tattoos, extra marks, wounds, redness, tools, lacquer, board, labels, text, grid or watermark. No face. Single image, not collage; landscape 3:2, identical realistic photographic treatment to input.
```

## H01_left_hand.png

编号：H01；左手独立参考；实际尺寸：1536×1024。

输入参考：02_视觉资产/H01_hands_master.png

```text
Use case: identity-preserve. Input is the H01 SAME PERSON hand identity master. Make ONE photorealistic standalone reference photograph of only the anatomical LEFT HAND that is on the LEFT HALF of the input. Preserve this exact hand's skin tone, nail shapes, finger proportions, natural knuckles and the same light-gray cotton cuff construction. Remove the other hand. Center the single left hand palm-down on the same charcoal-gray mat, wrist enters from bottom edge, all FIVE fingers fully visible with natural relaxed separation; in this top-down hand-back view the LEFT THUMB is on IMAGE RIGHT. Do not mirror the right-hand picture. Same soft left daylight and natural exposure. No jewelry, no watch, no tattoos, extra marks, wounds, redness, tools, lacquer, board, labels, text, grid or watermark. No face. Single image, not collage; landscape 3:2, identical realistic photographic treatment to input.
```

## H01_below_shoulders.png

编号：H01；肩以下身体与工作服；实际尺寸：1672×941。

输入参考：05_制作记录/候选与退回/H01_below_shoulders_v1_袖口待统一.png；02_视觉资产/H01_hands_master.png

```text
Use case: precise-object-edit and identity-preserve. Asset type: anonymous artisan below-shoulders reference for a contemporary lacquer craft film. Image 1 is the edit target; Image 2 is the EXACT hand identity and sleeve-cuff reference. Preserve image 1 composition, camera crop with no visible face or head, person's pose, light gray cotton work shirt including the existing front and collar, left window and cabinet, bench, mat, objects and lighting. Change ONLY the sleeve ends and hands to match image 2. The wrists must have the SAME broad plain light gray woven cotton cuff ends, with a narrow horizontal stitched hem and soft natural folds as image 2; no visible cuff buttons, no ribbed knit, no elastic wristbands and no rolled-up sleeves. Keep the hands resting at the same two positions on the far edge of the mat. Match the same natural skin tone, finger proportions and short natural nails of the pair of hands in image 2; no exaggerated veins, aging, jewelry or identifying marks. Anatomically correct five fingers on each hand, natural thumb orientation; right and left remain correct, do not mirror. Keep face completely outside image, head not visible, anonymous ordinary 25-35 year old operator. No new props, lacquer board, text or logos. Same understated realistic photograph, same landscape 16:9 canvas. The target is exact hand-and-cuff continuity with image 2 while retaining the scene.
```

## G01_plum_layout.png

编号：G01；三朵金梅布局参考；实际尺寸：1536×1024。

输入参考：无，文字生成。

```text
Use case: scientific-educational. Asset type: FLAT ORTHOGRAPHIC DESIGN TEMPLATE, NOT a photograph, NOT a rendering, NOT transparent. A clean solid pure WHITE (#FFFFFF) 3:2 landscape canvas, with a small plum branch line drawing confined to its lower right quarter. Exactly THREE small simple five-petal plum blossoms connected to one branch with one fork. Branch begins near bottom right(95%,94%) and reaches up-left to(64%,61%); flowers centered roughly(72%,66%),(84%,78%),(91%,62%). All linework is ONE flat solid muted ochre color #A8823F. Clear sharp edges with thin elegant strokes, small sparse stamens. Flower interiors stay WHITE. Huge WHITE negative space above and left. This is a flat color layout stencil used as a reference for later gold painting on lacquer, so absolutely NO lighting, no three-dimensional metal, no gradient, no glow, no bloom, no cast shadow, no grain, no paper texture. White background must remain equally white immediately next to every gold stroke; no tinted halo. No words, borders, coordinate marks, frames, boards, other flowers, buds, leaves, birds or symbols. One image, no panels.
```

## P01_wood_top.png

编号：P01；裸木胎俯视；实际尺寸：1536×1024。

输入参考：05_制作记录/候选与退回/P01_top_v1_比例待校正.png

```text
Use case: precise-object-edit. Correct ONLY the wood blank's shape to a TRUE 3:2 WIDTH:HEIGHT rectangle in this exact overhead photo. It is presently a little too wide for its height. Keep horizontal width the same and increase its top-to-bottom dimension slightly until it is exactly1.5 times as wide as tall; a board about30cm wide and20cm tall. Keep the board centered on the SAME gray mat, the same wood grain, tiny corner rounding, soft left lighting and brown table. The top and bottom board edges must remain straight and parallel, no perspective since this is straight top-down. Approximate target within a1536x1024 canvas: board from x=318 to1218 (900px), y=212 to812 (600px), about3:2. No drawn pixel coordinates or dimension annotations in image. It remains a very thin plain wood blank, about1cm thick, no rim, recess, box, holes, red paint, black lacquer, gold pattern or tools or hands. Change only this small geometry correction and preserve the photographic realism. ONE single full photo, not a sheet or diagram.
```

## P01_wood_oblique.png

编号：P01；裸木胎斜俯视；实际尺寸：1536×1024。

输入参考：02_视觉资产/P01_wood_top.png

```text
Use case: precise-object-edit. Input is the locked P01 wood geometry master. Create an oblique-camera reference of the EXACT SAME thin wood board, same charcoal mat and brown bench, same clean pale fine grain and slightly rounded corners. Change only the viewpoint from straight overhead to a stable, centered three-quarter overhead product view about55 degrees above the tabletop; the camera faces the board symmetrically so the long edges remain horizontal and the far edge recedes naturally. Keep physical width:depth at30:20cm, thickness about1cm; show the thin front edge, NOT a box or tray, no lip or recess. Entire board clearly visible, occupies about70% of image width, generous gray mat around it. Same soft left window illumination, readable shadows, photorealistic restrained workshop look. No hands, tools, gold, black lacquer, red side paint, labels, lines, annotation, extra objects, haze or watermarks. One landscape3:2 image. This will be the fixed camera basis for the later lacquer surface states; keep simple stable perspective.
```

## P02_cloth.png

编号：P02；裱布状态；实际尺寸：1536×1024。

输入参考：02_视觉资产/P01_wood_top.png

```text
Use case: precise-object-edit. Input is the locked straight-overhead P01 wood board reference. Change ONLY its upper surface into the CLOTH-LINING stage: one thin layer of natural off-white open-weave gauze neatly adhered flat over the same wood blank. Fine but visible warp and weft fibers, restrained natural off-white, taut and smooth without folds, full-width cloth covering board, slight wood or folded-fiber at thin edges plausible. It is a flat textile layer bonded to the board, not loose fabric floating over it and not a separate towel. NO gray filler yet, no liquid, no gold, no black lacquer, no red paint. Preserve EXACT board silhouette,3:2 proportion, size in frame, corner rounding, same gray mat, brown table grain, camera crop and soft left daylight. No hands, tools, typography, new objects, watermarks or airborne dust. One photorealistic landscape image matching input.
```

## P02_gray_wet.png

编号：P02；湿灰胎状态；实际尺寸：1536×1024。

输入参考：02_视觉资产/P02_cloth.png

```text
Use case: precise-object-edit. Input is the same P02 cloth-lined flat board. Change ONLY its TOP SURFACE to the wet filler/gray-ground preparation stage: a thin continuous layer of natural warm-gray fine lacquer putty coats the gauze, with just a few restrained shallow flat-spatula spreading tracks indicating it is still a workable paste. Most fabric weave is covered. It is smooth fine putty, NOT rough cement, gravel, thick mud, running water, glossy resin, or modeling clay lumps. Preserve the exact thin board outline, corner shape, position, size, overhead camera, charcoal mat and brown table pattern from input. No metal tools or hands baked into reference. No black lacquer yet, no gold or red decoration, no lettering, measures, extra objects, haze or watermark. Same soft LEFT daylight; natural material color, photorealistic texture, one single landscape production reference.
```

## P02_gray_cured.png

编号：P02；已干固灰胎；实际尺寸：1536×1024。

输入参考：02_视觉资产/P02_gray_wet.png

```text
Use case: precise-object-edit. Input shows wet fine gray-ground putty over a thin cloth-lined board. Make ONLY the dry cured and smoothed state of THAT SAME filler surface. Remove all wet spreading ridges, spatula tracks and all visible woven-fabric fibers: the gauze is BURIED under a continuous opaque warm-gray lacquer-ground layer, so the surface is now a uniform fine dense MATTE SOLID, like very fine dry clay ground, NOT cloth or canvas. A barely perceptible fine mineral texture is allowed, but no cross-hatch weave. Keep exactly the input's warm-gray hue, thin board outline, same corner shape,3:2 geometry, position, top-down camera, size, mat, table pattern and left lighting. Do not turn it into thick stone, a tray or white plaster slab. No cracks, loose dust, big scratches, wet sheen, gold, black lacquer, red paint, hands, tools or text. Change only the ground surface becoming dry, smooth and solid. Photorealistic material-stage reference.
```

## P03_black_cured.png

编号：P03；固化无纹黑漆底；实际尺寸：1536×1024。

输入参考：02_视觉资产/P01_wood_oblique.png

```text
Use case: precise-object-edit. Input is the locked oblique P01 board/camera master. Change ONLY the board material to the unadorned CURED BLACK LACQUER stage P03. Preserve exactly the same thin flat rectangular geometry,3:2 physical shape, slightly rounded corners, position, perspective, scale, table wood grain, charcoal mat and soft left daylight. Cover the top evenly with deep neutral BLACK cured lacquer, already smooth with a modest controlled natural sheen, not a perfect mirror yet. The THIN VERTICAL SIDE EDGE only becomes muted dark vermilion red; no red border on the top, no raised rim or tray shape. NO gold decoration anywhere, no painting, no lines or blossoms. No liquid pooling, no visible oil, ash, scratches, tools, hands or dust. Black must remain black, not gray metal or glass. Fine realistic lacquer material, calm restrained contemporary craft photography. Keep everything outside the board unchanged. One landscape image.
```

## P04_gold_partial_branch.png

编号：P04；描金局部：梅枝；实际尺寸：1536×1024。

输入参考：02_视觉资产/P04_gold_complete.png

```text
Use case: precise-object-edit. Input is the LOCKED completed gold-plum board. Make the earlier branch-drawing progress state for shot12 by REMOVING gold paint only. Keep the exact input board geometry, black lacquer, red side edge, camera, mat, table, light and background untouched. Keep the LOWER MAIN GOLD STEM from bottom-right corner up toward its first main fork, plus one small incomplete branch segment; REMOVE ALL THREE flower outlines and stamens and remove upper twig portions not yet drawn. Where gold is removed, restore exactly the same smooth black lacquer, no ghost blossoms or gray traces. Do not shift or redesign the surviving main branch: it must be a literal subset of input gold coordinates and shape. This is incomplete painted progress, no brush or hands baked in, no new marks, no buds, no other decoration. Flat thin antique gold paint, not glowing or embossed. One same-camera photorealistic production-state image; more than85% of board remains plain black.
```

## P04_gold_partial_flower.png

编号：P04；描金局部：花瓣收笔；实际尺寸：1536×1024。

输入参考：02_视觉资产/P04_gold_complete.png

```text
Use case: precise-object-edit. Input is the LOCKED completed gold-plum board. Make a nearly-finished flower-drawing progress state for shot13, changing ONLY a tiny part of the gold linework. Keep the complete existing branch and TWO blossoms (the top-right blossom and lower-right blossom) exactly unchanged. In the LEFTMOST blossom, remove a small curved segment from ONE upper-right petal and a few of that blossom's central stamen marks, leaving a clear tiny place for the final brush stroke. Do not remove or shift entire flowers. The three flower positions, all surviving branch and petal coordinates, image crop, black lacquer, red side, mat, table and illumination must stay unchanged. Restore black under the missing gold stroke; no gray guide lines or white gap. NO hand or brush, text, new paint, frame or glow. One photorealistic fixed-camera progress-state image, same resolution and photographic composition as input.
```

## P04_gold_complete.png

编号：P04；三朵金梅完成母图；实际尺寸：1536×1024。

输入参考：02_视觉资产/P03_black_cured.png；02_视觉资产/G01_plum_layout.png

```text
Use case: compositing. Input1 is the EXACT LOCKED board photo, camera, black lacquer, thin dark vermilion side, gray mat and brown table. Input2 is ONLY the gold plum DESIGN reference; its WHITE background must not appear. Edit input1 by painting ONLY that same one plum motif as delicate FLAT GOLD LINEWORK on the LOWER RIGHT QUARTER of the board. Scale the ENTIRE motif from input2 down to fit inside the board's rightmost35% and bottom45%, all three five-petal flowers visible, branch starts near the board's bottom-right corner and forks up-left as in input2. Preserve branch topology, blossom shapes and order, exactly THREE blossoms. The rest of the board, at least75%, remains undecorated BLACK. No large flower, no motif at top right, no additional leaves, buds, birds, mountains or frame. This is completed thin painted gold decoration, NOT embossed metal, no white patch, no gold glow, no shadows from the flat design. Preserve input1 EXACT geometry, edges, camera position, frame, outside table/mat, illumination and base sheen. Do not add new reflections or alter background. No tools, hands, text, watermark or scene change. One photorealistic image; input1 dominates composition and input2 supplies only rescaled gold strokes.
```

## P05_coat_structure.png

编号：P05；罩漆器型与纹样结构母图；实际尺寸：1536×1024。

输入参考：02_视觉资产/P04_gold_complete.png

```text
Use case: precise-object-edit. Input is the LOCKED completed gold-plum board and exact fixed camera. Change ONLY the surface finish to the clear OVERCOAT structure state P05: the same black lacquer and exactly the same three-blossom gold drawing are now under a very thin continuous transparent refined-lacquer coating. Preserve every gold branch/petal coordinate, its visibility and position. The new coating has a restrained slightly more unified soft surface sheen, not a thick glass layer, not epoxy flooding, no droplets or drips. Black stays deep black and the painted gold remains flat beneath the surface, no extrusion or glow. Keep exact board outline and thin dark-red side, perspective, frame, table grain, charcoal mat, light direction and overall exposure. Do not add clear sharp white window reflections yet; only subtle naturally reflected left-side light. No sanding scratches, oil, ash, tools, hands, text or watermark. One photorealistic structural master, not an infographic or labeled diagram.
```

## P05A_coat_cured.png

编号：P05A；罩层已固化、待精磨；实际尺寸：1536×1024。

输入参考：02_视觉资产/P05_coat_structure.png

```text
Use case: precise-object-edit. Input is the locked P05 overcoated lacquer board. Make P05A: the same very thin clear lacquer overcoat is now FULLY CURED, ready for fine wet sanding. Preserve exact board outline, red thin side, three gold flower design and every branch/petal coordinate, same camera/crop, gray mat and brown table pattern, overall exposure and LEFT light direction. The black finish is solid, smooth and mildly satin-gloss with only the same broad soft reflected light, no wet fluid, drips, oil, powder, tools, hands or sanding scratches. Do not invent a sharp mirror/window reflection or make a dramatic brighter/darker version; this is a subtle material-state reference, not a magic transformation. Gold remains beneath the clear coat, not raised. One photorealistic fixed-camera image with all background details retained.
```

## P05B_finely_sanded.png

编号：P05B；精磨后、已清理；实际尺寸：1536×1024。

输入参考：02_视觉资产/P05_coat_structure.png

```text
Use case: precise-object-edit. Input is the locked overcoated black/gold lacquer board. Change ONLY its clear top-coat surface into the just-FINELY-SANDED AND CLEANED preparation state P05B, prior to oil and fine ash. A very fine even satin/matte haze from microscopic surface roughness softly diffuses the left light, while black stays BLACK, not white/gray paint or metal. No visible coarse scratches, no directional gouges, no sanding through gold, no white residue: the surface is clean and dry, pattern still fully visible underneath. Keep the identical three-blossom gold layout, board geometry, red side thickness, position, perspective, mat/table textures, crop and exposure. No oil yet, no powder, water puddles, hands, tools or text. This is physical fine sanding at a subtle scale, not a frosted glass or thick plastic sheet. One photorealistic fixed-camera state reference.
```

## P05B_oiled.png

编号：P05B；薄擦麻油后、尚未落灰；实际尺寸：1536×1024。

输入参考：02_视觉资产/P05B_finely_sanded.png

```text
Edit this exact still image as a precise continuity reference for a lacquer craft film. Preserve the entire image: identical camera viewpoint, board outline and size and position, perspective, gently rounded corners, thin vermilion red side, charcoal work mat, brown wooden table, lighting, same three gold plum flowers and every branch coordinate. Change ONLY the state of the black lacquer top: it has just been wiped with an extremely thin even film of natural sesame oil in preparation for palm polishing. Show a subtle restrained satin oily sheen, very slight, no puddles or drops or streaks, no thickness, no extra reflectors or window image. It is still finely sanded, not a glossy finished mirror. Keep gold completely unchanged and unobscured. No brick ash yet. No hands, tools, text, logos, particles, glow or magical effect. Full single photographic frame, same 3:2 canvas. This is a staged AI visual reference, ordinary contemporary craft realism.
```

## P05C_oil_ash.png

编号：P05C；薄油与少量细砖灰操作面；实际尺寸：1536×1024。

输入参考：02_视觉资产/P05B_oiled.png

```text
Use case: precise-object-edit. Asset type: one still continuity reference for a lacquer palm-polishing film. Input image 1 is the exact edit target. Keep the board geometry, camera viewpoint, black top, red thin side edge, table, mat, lighting and every gold branch and exactly three flowers completely unchanged. The board already has a very thin wiped sesame-oil film; retain it. Add ONLY a small restrained amount of extremely finely levigated brick ash to a compact working patch in the lower left/center-left black area, away from the gold pattern: sparse warm muted light gray-brown micron-like fine powder, low density, a lightly dispersed dusting in contact with the surface, a few faint curved wipe traces suggesting the start of palm polishing. The majority of black lacquer stays visibly black and open, gold is fully visible. Not a heap, no granular chunks, not sand, no thick flour coating, no opaque paste or dirty stains. No floating dust, no flying particles. No hand or tool baked into this reference still: those will be introduced in video. Do not make the board a mirror, do not add window reflection. This is the oiled and lightly ash-dusted working state, not a clean inspection state. Single photographic image, same 3:2 canvas, no labels, text, logos, split panels or collage.
```

## C01_mid_polish_check.png

编号：C01；掌推中途、整理后的检查面；实际尺寸：1536×1024。

输入参考：02_视觉资产/P05_coat_structure.png

```text
Use case: precise-object-edit. Input is the LOCKED same board, gold design, camera and background. Make C01, the intermediate polish INSPECTION BASELINE after necessary cleaning, no hands. Preserve all geometry, board angle/size, same thin vermilion edge, same exact three gold blossoms/petals, mat, table wood grain, focus and overall exposure. Add ONE restrained reflection of a SMALL SECTION of the existing LEFT wooden window on the UPPER LEFT black area of the board, clear of the gold design. The reflected patch has two columns by two rows of pale neutral daylight separated by a simple dark wooden cross, projected plausibly onto the flat board plane. It is a soft slightly diffuse, hazy-edged reflection due to subtle remaining surface scatter; the four panes and outer boundary can still be recognized. Not a reflection of clouds, sky/trees or a whole courtyard. Keep the overall black dark, no glowing lacquer, no spotlight or lens flare. Reflection is medium gray-white, not clipped pure white. Board clean and dry: no powder, oil smear, fingerprints, scratches, dust, tools or people. Everything outside that reflected-light patch should remain unchanged. This exact image will be edited into C02 with ONLY sharper reflection edges, so use a stable simple reproducible shape.
```

## C02_finished_check.png

编号：C02；完成检查面；实际尺寸：1536×1024。

输入参考：02_视觉资产/C01_mid_polish_check.png

```text
Make one extremely controlled edit to this exact photographic still, the completed state of the same lacquer panel after further palm polishing. Keep the source image composition, camera, board geometry, rounded corners, thickness, red side edge, gold plum pattern with exactly the same three flowers and branch coordinates, tabletop and mat texture, exposure, light direction, focus and colors identical. Keep the existing reflected window in the exact same upper left area of the black board, same outer shape, same single vertical and horizontal cross bars, same perspective and brightness. Change ONLY the surface scattering of that existing window reflection: its edges become noticeably sharper and cleaner while retaining natural restrained reflection contrast. Use crisp narrow edges on the same reflected cross and panes, not new window panes, not a larger or moved reflection. Black lacquer remains black, no overall brightening, no white blown highlights. Both states are clean inspection states with no powder or visible residual oil, so do not change cleanliness or add/remove anything. No text, hands, tools, particles, glow, lens effects. Same 3:2 canvas. Deliver one faithful matched final-state reference, not a side-by-side collage.
```

## K01_palm_contact.png

编号：K01；右掌接触、左手稳板；实际尺寸：1672×941。

输入参考：02_视觉资产/P05C_oil_ash.png；02_视觉资产/H01_hands_master.png

```text
Use case: compositing and identity-preserve. Asset type: K01 palm-contact action keyframe for a contemporary Chinese lacquer craft film. Image 1 is the exact scene, board and oiled finely dusted working state to preserve. Image 2 is the exact pair of hands and light gray woven cotton cuffs to insert. Create one realistic landscape photograph, widen to 16:9 without cropping the board. Keep the same flat rectangular board, perspective, gently rounded corners, thin red side edge, all three gold plum blossoms and branches in their exact right-lower coordinates, same brown bench and charcoal mat. Add the same anonymous operator's hands entering from the lower edge only, no face or body. The RIGHT hand reaches from lower right and lies palm-down in genuine full contact with the center-left black working area, fingertips pointing gently away from the operator; back of hand visible. LEFT hand from lower left gently stabilizes the left board edge, not the decorated area. Anatomically natural right and left thumb orientations; five digits on each hand, no duplication or merged fingers. Forearms do not cross. Natural short nails, no jewelry, light gray plain cotton stitched cuffs matching image 2, no rib-knit or buttons at cuffs. Keep the existing very small amount of fine muted gray-brown brick ash close to the contact area, not covering the board, no floating particles. This is contact at the start of one short straight palm stroke, not a dramatic grinding pose. Gold remains visible and untouched. No hand penetrating or fused into the board, no red swollen skin, no new tools, no text or glow. Contact, credible weight and skin compression matter more than beauty posing. Keep the original camera angle, exposure and lighting.
```

## K02_almost_putaway.png

编号：K02；棉团将放回小碟却停住；实际尺寸：1671×941。

输入参考：02_视觉资产/K01_palm_contact.png；02_视觉资产/C01_mid_polish_check.png；02_视觉资产/R01_initial_detail.png

```text
Use case: precise-object-edit and identity-preserve. Asset type: K02 interrupted tidying action keyframe. Image 1 is the exact scene, board geometry, gold pattern, hand identity and camera to edit. Image 2 is ONLY the cleaned intermediate inspection material state, not a geometry replacement. Image 3 is ONLY the soft reflection quality. Keep image 1's board position and outline, all THREE gold plum flowers and branch coordinates, red thin side, charcoal mat and brown tabletop. Preserve its left hand gently stabilizing the left edge. Repose the RIGHT hand naturally at the lower-right side OUTSIDE the board, holding a small ordinary off-white cotton wad between thumb and fingers, poised 2-3cm above one small shallow matte charcoal-gray ceramic dish resting on the work mat to the right of the board. The forearm still enters from lower right, same plain light gray cotton stitched cuff, short nails, no jewelry. It is about to put the cotton away but has PAUSED just before touching the dish; cotton stays in the fingers. Natural anatomy with five fingers, no floating disconnected hand, no crossing arms. Change board material from the dusty working state to the clean inspection state of image 2: no ash or oil residue; include a restrained soft-edged reflected window in the upper left black area, same source and four-pane partial grid. This is a new shot AFTER an editorial omission of surface preparation, not an automatic on-screen cleaning effect. The board remains black, no glow or overexposure. Dish is a plain contemporary tidying prop, not an alleged traditional tool. No extra brush, lid, tool box, text, logo or face. One 16:9 photograph with board and dish fully readable, same camera and lighting as image 1.
```

## K04_finished_before_putaway.png

编号：K04；完成表面、仍持棉团；实际尺寸：1671×941。

输入参考：02_视觉资产/K02_almost_putaway.png；02_视觉资产/K03_final_putaway.png

```text
Use case: precise-object-edit. Asset type: K04 matched beginning keyframe for the FINAL putting-away gesture. Image 1 is the EXACT target frame: right hand holding the cotton above the small dish, left hand stabilizing the board. Image 2 is the finished reflection appearance to match. Make ONLY ONE change to image 1: refine the existing window reflection's soft edges to the finished more even definition of image 2. Keep the same reflected window size, shape, cross bars, perspective, location and brightness, same exposure and black material color. Preserve all other contents and positions exactly as image 1: cotton remains PINCHED in the right fingers, above the dish, not resting inside it; same right-hand pose, natural five fingers, gray cotton stitched cuff, same left hand, same board outline and placement, three gold plum blossoms and every branch, red side edge, gray mat, tabletop and ceramic dish. No cleaning change, no added oil, powder, particles, labels or glow. This is AFTER polishing, just before cotton is put away. It must pair with image 2 as an actual hand-action start/end, with the lacquer reflection ALREADY finished and unchanged throughout that gesture. Do not use image 2's relaxed right-hand pose or cotton-in-dish position yet. One single same 16:9 image, not a collage.
```

## K03_final_putaway.png

编号：K03；棉团已归置、手将撤开；实际尺寸：1671×941。

输入参考：02_视觉资产/K02_almost_putaway.png；02_视觉资产/C02_finished_check.png

```text
Use case: precise-object-edit and identity-preserve. Asset type: K03 completion of the same interrupted tidying gesture. Image 1 is the EXACT edit target. Image 2 provides ONLY the finished lacquer reflection quality, not scene geometry. Preserve image 1 camera, entire tabletop and work mat, board outline and position, red edge, ALL THREE gold flowers and every branch, left window-reflection shape and perspective, lighting and exposure, ceramic dish position and size, cotton appearance, operator's skin and cuffs. Make only two limited completion changes. First, the SAME small cotton wad is now resting inside the SAME shallow gray dish at the right, and the RIGHT hand has just released it: fingers are naturally relaxed 2-3cm above it, no longer pinching or touching cotton, withdrawing toward lower right. The left hand is slightly relaxed beside the left board edge, with no continued polishing. Five fingers per hand, natural anatomy, no jewelry. Second, the same existing reflected window on the clean black board now has more evenly defined edges, like image 2, but keep its location, grid and brightness exactly as image 1. No powder, oil residue or change in cleanliness in either shot. This is a new final shot after polishing and an inspection, NOT continuous magical surface transformation. Do not move the dish, put new objects in it, add a lid, add tools or change the shirt cuffs. Black stays black. No glow, text, extra gold, people or face. Same 16:9 frame. The visual narrative is the SAME putting-away action finally completed, with no more work beginning.
```

## R01_initial_detail.png

编号：R01；第一次检查：窗影边缘发散；实际尺寸：1536×1024。

输入参考：02_视觉资产/C01_mid_polish_check.png

```text
Use case: precise-object-edit. Asset type: R01 close inspection reference, initial state, for a restrained realistic AI lacquer craft film. Image 1 is the exact source object and reflection. Make one tightly framed photographic close-up of the same board's left inspection region. Enlarge the existing window reflection so it is plainly readable on a phone: it should occupy roughly the left third of the frame. Crop away most of the surrounding work mat and tabletop. Retain a thin portion of the straight muted vermilion front edge along the bottom as a sharp focus and geometry reference; at the far right allow only the naturally cropped existing gold plum pattern, never redesign or add blossoms. The black surface should nearly fill the image. Keep the source window geometry, exactly one vertical and one horizontal cross bar forming four reflected panes, the same perspective and restrained brightness. Preserve the existing soft scattered edges of the reflection, neither a foggy dirty surface nor a pristine finished mirror. The physical red edge and visible gold strokes remain sharp, proving the surface reflection is diffuse rather than a camera-focus effect. No ash, dust, oil puddle, scratches, cracks or visible contamination. Do not invent a damaged patch. Same natural left-window lighting and exposure; black remains black, no glow. One clean 3:2 photographic frame, no hands, labels, diagram, split comparison or text. This first selected close-up will be the exact geometry master for intermediate and finished inspection edits.
```

## R02_progress_detail.png

编号：R02；中途检查：局部改善、仍有发散；实际尺寸：1536×1024。

输入参考：02_视觉资产/R01_initial_detail.png

```text
Use case: precise-object-edit. Image 1 is the exact locked inspection close-up. Produce the intermediate progress state R02. Preserve every pixel-level compositional relationship: same fixed camera, black lacquer geometry, straight red front edge, cropped gold flower and branch coordinates, SAME reflected window and its exact four panes, cross bars, location, perspective, brightness and sizes. Same focus, exposure and surface cleanliness, no powder or visible oil in either state. Change ONLY the surface scattering near the existing reflected window: compared with this initial image, make the upper reflected pane edges and upper section of the dark vertical cross bar moderately clearer, but retain a visibly soft scattered edge in the lower reflected area. This is partial progress; it must remain intermediate between soft reflection and evenly crisp reflection. Do not change the shape of the window or add a stripe or defect, don't brighten the image or sharpen the actual painted gold and edge. Do not add hands, labels, diagrams or particles. The actual board edge and gold remain as sharp as in the source. It is an artistically staged surface-scattering reference, not a real material experiment. One single matching 3:2 image, not a comparison sheet.
```

## R03_finished_detail.png

编号：R03；最终检查：反射更均匀清楚；实际尺寸：1536×1024。

输入参考：02_视觉资产/R01_initial_detail.png

```text
Use case: precise-object-edit. Image 1 is the exact locked inspection close-up R01. Produce the finished state R03 by changing ONLY the surface scattering of the same existing reflected window. Keep the entire frame otherwise identical: camera crop, black board geometry, straight red front edge, every cropped gold plum flower and branch coordinate, actual object focus, brightness, exposure, color, fine surface cleanliness, and the exact reflected four window panes with one vertical and one horizontal cross bar in the same perspective and location. Narrow the blurred transition along ALL existing window-reflection boundaries so they read as an evenly clear natural window reflection. Keep original contrast and restrained pane brightness as closely as possible; do not make the reflected window larger, whiter, moved, or a different grid. Never add more panes or specular dots. Black stays black, no glow, no global brightening. Both reference and finished state have no powder or visible residual oil; no cleaning change. Red edge and gold are already in focus and must not sharpen or move. No hands, labels, particles, fog or text. A single faithful 3:2 matched image, not a collage; the only clear visual change is less surface scattering and a more evenly defined reflected window.
```

